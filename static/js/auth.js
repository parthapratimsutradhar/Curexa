// // -----------------------------
// // Utils: Cookie helpers
// // -----------------------------
// function getCookie(name) {
//     const match = document.cookie.match(new RegExp('(^| )' + name + '=([^;]+)'));
//     return match ? match[2] : null;
// }

// // -----------------------------
// // Decode JWT payload
// // -----------------------------
// function decodeToken(token) {
//     try {
//         return JSON.parse(atob(token.split(".")[1]));
//     } catch (err) {
//         return null;
//     }
// }

// // -----------------------------
// // Check if token expired
// // -----------------------------
// function isTokenExpired(token) {
//     const payload = decodeToken(token);
//     if (!payload) return true;
//     const now = Math.floor(Date.now() / 1000);
//     return payload.exp < now;
// }

// // -----------------------------
// // Refresh Access Token (httpOnly refresh token)
// // -----------------------------
// async function refreshAccessToken() {
//     try {
//         const res = await fetch("/api/token/refresh/", {
//             method: "POST",
//             headers: { "Content-Type": "application/json" },
//             credentials: "include", // important: sends httpOnly cookie
//         });

//         if (!res.ok) throw new Error("Failed to refresh token");

//         const data = await res.json();
//         // data.access contains new access token
//         document.cookie = `access_token=${data.access}; max-age=${30*60}; path=/; SameSite=Lax; Secure`;
//         return data.access;
//     } catch (err) {
//         console.error("Token refresh failed:", err);
//         return null;
//     }
// }

// // -----------------------------
// // API fetch wrapper
// // -----------------------------
// async function apiFetch(url, options = {}) {
//     let accessToken = getCookie("access_token");

//     if (!accessToken || isTokenExpired(accessToken)) {
//         accessToken = await refreshAccessToken();
//         if (!accessToken) throw new Error("User needs to log in again");
//     }

//     options.headers = {
//         ...options.headers,
//         Authorization: `Bearer ${accessToken}`,
//         "Content-Type": "application/json"
//     };

//     const res = await fetch(url, options);
//     if (!res.ok) throw new Error("API request failed");
//     return res.json();
// }

// // -----------------------------
// // Silent pre-expiry refresh
// // -----------------------------
// function scheduleSilentRefresh() {
//     const accessToken = getCookie("access_token");
//     if (!accessToken) return;

//     const payload = decodeToken(accessToken);
//     if (!payload || !payload.exp) return;

//     const now = Math.floor(Date.now() / 1000);
//     const msBeforeExpiry = (payload.exp - now - 60) * 1000; // refresh 1 min before expiry

//     setTimeout(async () => {
//         const newToken = await refreshAccessToken();
//         if (!newToken) {
//             console.warn("User needs to log in again");
//             // optionally redirect to login page
//         } else {
//             scheduleSilentRefresh(); // schedule next refresh
//         }
//     }, Math.max(msBeforeExpiry, 0));
// }

// // -----------------------------
// // Initialize on page load
// // -----------------------------
// window.addEventListener("load", () => {
//     scheduleSilentRefresh();
// });