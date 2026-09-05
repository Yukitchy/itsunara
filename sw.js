// 最小のService Worker: インストール即有効化・fetchは素通し（PWAとして成立させるためだけ）
self.addEventListener('install', function (e) { self.skipWaiting(); });
self.addEventListener('activate', function (e) { e.waitUntil(self.clients.claim()); });
self.addEventListener('fetch', function (e) { /* passthrough */ });
