from django.urls import get_resolver, reverse, NoReverseMatch

from apps.core.utilities.route_metadata import (
    AUTH_LABELS,
    CATEGORY_CONFIG,
    METHOD_COLORS,
    ROUTE_METADATA,
)


def _pattern_str(pattern):
    return str(getattr(pattern, "pattern", pattern))


def _view_name(callback):
    if hasattr(callback, "cls"):
        return callback.cls.__name__
    if hasattr(callback, "view_class"):
        return callback.view_class.__name__
    return getattr(callback, "__name__", str(callback))


def _collect_patterns(patterns, prefix=""):
    routes = []
    for pattern in patterns:
        if hasattr(pattern, "url_patterns"):
            sub_prefix = prefix + _pattern_str(pattern.pattern)
            routes.extend(_collect_patterns(pattern.url_patterns, sub_prefix))
            continue

        path = prefix + _pattern_str(pattern.pattern)
        name = pattern.name or ""
        if name == "not_found_page":
            continue

        routes.append(
            {
                "path": "/" + path.lstrip("/"),
                "name": name,
                "view": _view_name(pattern.callback),
            }
        )
    return routes


def _normalize_path(path):
    if not path.startswith("/"):
        return "/" + path
    return path


def _categorize(path, name):
    clean_path = path.lstrip("/")
    for category in CATEGORY_CONFIG:
        if category["match"](clean_path, name):
            return category["id"]
    return "public"


def _infer_auth(path, name, meta):
    if meta.get("auth"):
        return meta["auth"]
    if path.startswith("/admin/") and "login" not in path:
        return "admin"
    if path.startswith("/doctor/") and "login" not in path:
        return "doctor"
    if path.startswith("/api/") and name in ("me", "auth-logout", "token_refresh"):
        return "authenticated"
    if path.startswith("/api/"):
        return "public"
    return "public"


def _infer_methods(path, name, meta, view_name):
    if meta.get("methods"):
        return meta["methods"]

    lower_view = view_name.lower()
    if "apiview" in lower_view or "viewset" in lower_view or path.startswith("/api/"):
        if "list" in name or "detail" in name:
            return ["GET", "POST", "PUT", "PATCH", "DELETE"]
        return ["GET", "POST"]

    if "delete" in name:
        return ["POST", "DELETE"]
    if "add" in name or "create" in name or "book" in name or "checkout" in name:
        return ["GET", "POST"]
    if "edit" in name or "update" in name:
        return ["GET", "POST", "PUT", "PATCH"]
    if "verify" in name or "send_otp" == name:
        return ["POST"]
    return ["GET"]


def _build_description(path, name, meta, view_name):
    if meta.get("description"):
        return meta["description"]

    readable_name = (name or view_name).replace("-", " ").replace("_", " ").title()
    if path.startswith("/api/"):
        return f"API endpoint — {readable_name}."
    if path.startswith("/admin/"):
        return f"Admin panel page — {readable_name}."
    if path.startswith("/doctor/"):
        return f"Doctor portal — {readable_name}."
    return f"Web page — {readable_name}."


def _resolve_url(name):
    if not name:
        return None
    try:
        return reverse(name)
    except NoReverseMatch:
        return None


def collect_all_routes():
    resolver = get_resolver()
    raw_routes = _collect_patterns(resolver.url_patterns)

    seen = set()
    enriched = []

    for route in raw_routes:
        path = _normalize_path(route["path"])
        dedupe_key = (path, route["name"])
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)

        name = route["name"]
        meta = ROUTE_METADATA.get(name, {})
        category_id = _categorize(path, name)
        auth = _infer_auth(path, name, meta)
        methods = _infer_methods(path, name, meta, route["view"])
        description = _build_description(path, name, meta, route["view"])

        enriched.append(
            {
                "path": path,
                "name": name or "—",
                "view": route["view"],
                "description": description,
                "methods": methods,
                "method_badges": [
                    {"name": m, "color": METHOD_COLORS.get(m, "#64748b")}
                    for m in methods
                ],
                "auth": auth,
                "auth_label": AUTH_LABELS.get(auth, AUTH_LABELS["public"]),
                "category": category_id,
                "resolved_url": _resolve_url(name) if name else path,
                "is_api": path.startswith("/api/"),
            }
        )

    enriched.sort(key=lambda r: (r["category"], r["path"]))
    return enriched


def build_route_docs_context():
    routes = collect_all_routes()
    categories = []

    for cat in CATEGORY_CONFIG:
        cat_routes = [r for r in routes if r["category"] == cat["id"]]
        if not cat_routes:
            continue
        categories.append(
            {
                "id": cat["id"],
                "label": cat["label"],
                "icon": cat["icon"],
                "color": cat["color"],
                "count": len(cat_routes),
                "routes": cat_routes,
            }
        )

    stats = {
        "total": len(routes),
        "web": len([r for r in routes if not r["is_api"]]),
        "api": len([r for r in routes if r["is_api"]]),
        "categories": len(categories),
    }

    return {
        "routes": routes,
        "categories": categories,
        "stats": stats,
    }
