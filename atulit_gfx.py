"""Shared graphics helpers for Atulit static sites: Lucide icons (ISC/MIT, https://lucide.dev),
brand favicons, hero illustrations, time based dark mode. Copied into each site repo; edit in atulit-graphics."""
import re, colorsys, html as _h
ICONS = {"tv": "<path d=\"m17 2-5 5-5-5\" /><rect width=\"20\" height=\"15\" x=\"2\" y=\"7\" rx=\"2\" />", "music": "<path d=\"M9 18V5l12-2v13\" /><circle cx=\"6\" cy=\"18\" r=\"3\" /><circle cx=\"18\" cy=\"16\" r=\"3\" />", "briefcase": "<path d=\"M16 20V4a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16\" /><rect width=\"20\" height=\"14\" x=\"2\" y=\"6\" rx=\"2\" />", "shopping-bag": "<path d=\"M16 10a4 4 0 0 1-8 0\" /><path d=\"M3.103 6.034h17.794\" /><path d=\"M3.4 5.467a2 2 0 0 0-.4 1.2V20a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6.667a2 2 0 0 0-.4-1.2l-2-2.667A2 2 0 0 0 17 2H7a2 2 0 0 0-1.6.8z\" />", "list-checks": "<path d=\"M13 5h8\" /><path d=\"M13 12h8\" /><path d=\"M13 19h8\" /><path d=\"m3 17 2 2 4-4\" /><path d=\"m3 7 2 2 4-4\" />", "circle-check": "<circle cx=\"12\" cy=\"12\" r=\"10\" /><path d=\"m16 9-5.5 5.5L8 12\" />", "badge-check": "<path d=\"M3.85 8.62a4 4 0 0 1 4.78-4.77 4 4 0 0 1 6.74 0 4 4 0 0 1 4.78 4.78 4 4 0 0 1 0 6.74 4 4 0 0 1-4.77 4.78 4 4 0 0 1-6.75 0 4 4 0 0 1-4.78-4.77 4 4 0 0 1 0-6.76Z\" /><path d=\"m16 9-5.5 5.5L8 12\" />", "tag": "<path d=\"M12.586 2.586A2 2 0 0 0 11.172 2H4a2 2 0 0 0-2 2v7.172a2 2 0 0 0 .586 1.414l8.704 8.704a2.426 2.426 0 0 0 3.42 0l6.58-6.58a2.426 2.426 0 0 0 0-3.42z\" /><circle cx=\"7.5\" cy=\"7.5\" r=\".5\" fill=\"currentColor\" />", "external-link": "<path d=\"M15 3h6v6\" /><path d=\"M10 14 21 3\" /><path d=\"M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6\" />", "clock": "<circle cx=\"12\" cy=\"12\" r=\"10\" /><path d=\"M12 6v6l4 2\" />", "calendar-check": "<path d=\"M8 2v3\" /><path d=\"M16 2v3\" /><rect x=\"3\" y=\"3\" width=\"18\" height=\"18\" rx=\"2\" /><path d=\"M3 9h18\" /><path d=\"m9 15 2 2 4-4\" />", "calendar-x": "<path d=\"M8 2v3\" /><path d=\"M16 2v3\" /><rect x=\"3\" y=\"3\" width=\"18\" height=\"18\" rx=\"2\" /><path d=\"M3 9h18\" /><path d=\"m14 13-4 4\" /><path d=\"m10 13 4 4\" />", "activity": "<path d=\"M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2\" />", "wrench": "<path d=\"M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.106-3.105c.32-.322.863-.22.983.218a6 6 0 0 1-8.259 7.057l-7.91 7.91a1 1 0 0 1-2.999-3l7.91-7.91a6 6 0 0 1 7.057-8.259c.438.12.54.662.219.984z\" />", "triangle-alert": "<path d=\"m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3\" /><path d=\"M12 9v4\" /><path d=\"M12 17h.01\" />", "wifi-off": "<path d=\"M12 20h.01\" /><path d=\"M8.5 16.429a5 5 0 0 1 7 0\" /><path d=\"M5 12.859a10 10 0 0 1 5.17-2.69\" /><path d=\"M19 12.859a10 10 0 0 0-2.007-1.523\" /><path d=\"M2 8.82a15 15 0 0 1 4.177-2.643\" /><path d=\"M22 8.82a15 15 0 0 0-11.288-3.764\" /><path d=\"m2 2 20 20\" />", "search": "<path d=\"m21 21-4.34-4.34\" /><circle cx=\"11\" cy=\"11\" r=\"8\" />", "server": "<rect width=\"20\" height=\"8\" x=\"2\" y=\"2\" rx=\"2\" ry=\"2\" /><rect width=\"20\" height=\"8\" x=\"2\" y=\"14\" rx=\"2\" ry=\"2\" /><line x1=\"6\" x2=\"6.01\" y1=\"6\" y2=\"6\" /><line x1=\"6\" x2=\"6.01\" y1=\"18\" y2=\"18\" />", "info": "<circle cx=\"12\" cy=\"12\" r=\"10\" /><path d=\"M12 16v-4\" /><path d=\"M12 8h.01\" />", "file-user": "<path d=\"M6 22a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h8a2.4 2.4 0 0 1 1.704.706l3.588 3.588A2.4 2.4 0 0 1 20 8v12a2 2 0 0 1-2 2z\" /><path d=\"M14 2v5a1 1 0 0 0 1 1h5\" /><path d=\"M16 22a4 4 0 0 0-8 0\" /><circle cx=\"12\" cy=\"15\" r=\"3\" />", "pen-tool": "<path d=\"m18 13-.654-4.736a4 4 0 00-2.756-3.266l-9.163-2.9a2 2 0 00-2.017.493l-.82.819a2 2 0 00-.492 2.017l2.9 9.163a4 4 0 003.266 2.756L13 18\" /><path d=\"M18.648 12.352a1.205 1.205 0 011.704 0l1.296 1.296a1.205 1.205 0 010 1.704l-6.296 6.296a1.205 1.205 0 01-1.704 0l-1.296-1.296a1.205 1.205 0 010-1.704z\" /><path d=\"m3 3 6.586 6.586\" /><circle cx=\"11\" cy=\"11\" r=\"2\" />", "clapperboard": "<path d=\"m12.296 3.464 3.02 3.956\" /><path d=\"M20.2 6 3 11l-.9-2.4c-.3-1.1.3-2.2 1.3-2.5l13.5-4c1.1-.3 2.2.3 2.5 1.3z\" /><path d=\"M3 11h18v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z\" /><path d=\"m6.18 5.276 3.1 3.899\" />", "graduation-cap": "<path d=\"M21.42 10.922a1 1 0 0 0-.019-1.838L12.83 5.18a2 2 0 0 0-1.66 0L2.6 9.08a1 1 0 0 0 0 1.832l8.57 3.908a2 2 0 0 0 1.66 0z\" /><path d=\"M22 10v6\" /><path d=\"M6 12.5V16a6 3 0 0 0 12 0v-3.5\" />", "pencil-line": "<path d=\"M13 21h8\" /><path d=\"m15 5 4 4\" /><path d=\"M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z\" />", "image": "<rect width=\"18\" height=\"18\" x=\"3\" y=\"3\" rx=\"2\" ry=\"2\" /><circle cx=\"9\" cy=\"9\" r=\"2\" /><path d=\"m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21\" />", "mic": "<path d=\"M12 19v3\" /><path d=\"M19 10v2a7 7 0 0 1-14 0v-2\" /><rect x=\"9\" y=\"2\" width=\"6\" height=\"13\" rx=\"3\" />", "code": "<path d=\"m16 18 6-6-6-6\" /><path d=\"m8 6-6 6 6 6\" />", "presentation": "<path d=\"M2 3h20\" /><path d=\"M21 3v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V3\" /><path d=\"m7 21 5-5 5 5\" />", "book-open-text": "<path d=\"M12 5v16\" /><path d=\"M16 13h2\" /><path d=\"M16 9h2\" /><path d=\"M20.001 19A2 2 0 0022 17V5a2 2 0 00-1.999-2L16 3.002A5 5 0 0012 5a5 5 0 00-4-2H4a2 2 0 00-2 2v12a2 2 0 001.999 2H8a5 5 0 014 2 5 5 0 014-2z\" /><path d=\"M6 13h2\" /><path d=\"M6 9h2\" />", "gift": "<path d=\"M12 7v14\" /><path d=\"M20 11v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2v-8\" /><path d=\"M7.5 7a1 1 0 0 1 0-5A4.8 8 0 0 1 12 7a4.8 8 0 0 1 4.5-5 1 1 0 0 1 0 5\" /><rect x=\"3\" y=\"7\" width=\"18\" height=\"4\" rx=\"1\" />", "zap": "<path d=\"M15.914 4a1.5 1.5 0 00-2.474-1.561l-9 9A1.5 1.5 0 005.5 14h4.002a.5.5 0 01.471.666L8.086 20a1.5 1.5 0 002.475 1.56l9-9A1.5 1.5 0 0018.5 10h-3.997a.5.5 0 01-.472-.667z\" />", "fan": "<path d=\"M10.827 16.379a6.082 6.082 0 0 1-8.618-7.002l5.412 1.45a6.082 6.082 0 0 1 7.002-8.618l-1.45 5.412a6.082 6.082 0 0 1 8.618 7.002l-5.412-1.45a6.082 6.082 0 0 1-7.002 8.618l1.45-5.412Z\" /><path d=\"M12 12v.01\" />", "hammer": "<path d=\"m15 12-9.373 9.373a1 1 0 0 1-3.001-3L12 9\" /><path d=\"m18 15 4-4\" /><path d=\"m21.5 11.5-1.914-1.914A2 2 0 0 1 19 8.172v-.344a2 2 0 0 0-.586-1.414l-1.657-1.657A6 6 0 0 0 12.516 3H9l1.243 1.243A6 6 0 0 1 12 8.485V10l2 2h1.172a2 2 0 0 1 1.414.586L18.5 14.5\" />", "sparkles": "<path d=\"M11.017 2.814a1 1 0 0 1 1.966 0l1.051 5.558a2 2 0 0 0 1.594 1.594l5.558 1.051a1 1 0 0 1 0 1.966l-5.558 1.051a2 2 0 0 0-1.594 1.594l-1.051 5.558a1 1 0 0 1-1.966 0l-1.051-5.558a2 2 0 0 0-1.594-1.594l-5.558-1.051a1 1 0 0 1 0-1.966l5.558-1.051a2 2 0 0 0 1.594-1.594z\" /><path d=\"M20 2v4\" /><path d=\"M22 4h-4\" /><circle cx=\"4\" cy=\"20\" r=\"2\" />", "truck": "<path d=\"M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2\" /><path d=\"M15 18H9\" /><path d=\"M19 18h2a1 1 0 0 0 1-1v-3.65a1 1 0 0 0-.22-.624l-3.48-4.35A1 1 0 0 0 17.52 8H14\" /><circle cx=\"17\" cy=\"18\" r=\"2\" /><circle cx=\"7\" cy=\"18\" r=\"2\" />", "paintbrush": "<path d=\"m14.622 17.897-10.68-2.913\" /><path d=\"M18.376 2.622a1 1 0 1 1 3.002 3.002L17.36 9.643a.5.5 0 0 0 0 .707l.944.944a2.41 2.41 0 0 1 0 3.408l-.944.944a.5.5 0 0 1-.707 0L8.354 7.348a.5.5 0 0 1 0-.707l.944-.944a2.41 2.41 0 0 1 3.408 0l.944.944a.5.5 0 0 0 .707 0z\" /><path d=\"M9 8c-1.804 2.71-3.97 3.46-6.583 3.948a.507.507 0 0 0-.302.819l7.32 8.883a1 1 0 0 0 1.185.204C12.735 20.405 16 16.792 16 15\" />", "paw-print": "<circle cx=\"11\" cy=\"4\" r=\"2\" /><circle cx=\"18\" cy=\"8\" r=\"2\" /><circle cx=\"20\" cy=\"16\" r=\"2\" /><path d=\"M9 10a5 5 0 0 1 5 5v3.5a3.5 3.5 0 0 1-6.84 1.045Q6.52 17.48 4.46 16.84A3.5 3.5 0 0 1 5.5 10Z\" />", "map-pin": "<path d=\"M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0\" /><circle cx=\"12\" cy=\"10\" r=\"3\" />", "calculator": "<rect width=\"16\" height=\"20\" x=\"4\" y=\"2\" rx=\"2\" /><line x1=\"8\" x2=\"16\" y1=\"6\" y2=\"6\" /><line x1=\"16\" x2=\"16\" y1=\"14\" y2=\"18\" /><path d=\"M16 10h.01\" /><path d=\"M12 10h.01\" /><path d=\"M8 10h.01\" /><path d=\"M12 14h.01\" /><path d=\"M8 14h.01\" /><path d=\"M12 18h.01\" /><path d=\"M8 18h.01\" />", "dollar-sign": "<line x1=\"12\" x2=\"12\" y1=\"2\" y2=\"22\" /><path d=\"M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6\" />", "dog": "<path d=\"M11.25 16.25h1.5L12 17z\" /><path d=\"M16 14v.5\" /><path d=\"M4.42 11.247A13.152 13.152 0 0 0 4 14.556C4 18.728 7.582 21 12 21s8-2.272 8-6.444a11.702 11.702 0 0 0-.493-3.309\" /><path d=\"M8 14v.5\" /><path d=\"M8.5 8.5c-.384 1.05-1.083 2.028-2.344 2.5-1.931.722-3.576-.297-3.656-1-.113-.994 1.177-6.53 4-7 1.923-.321 3.651.845 3.651 2.235A7.497 7.497 0 0 1 14 5.277c0-1.39 1.844-2.598 3.767-2.277 2.823.47 4.113 6.006 4 7-.08.703-1.725 1.722-3.656 1-1.261-.472-1.855-1.45-2.239-2.5\" />", "cat": "<path d=\"M12 5c.67 0 1.35.09 2 .26 1.78-2 5.03-2.84 6.42-2.26 1.4.58-.42 7-.42 7 .57 1.07 1 2.24 1 3.44C21 17.9 16.97 21 12 21s-9-3-9-7.56c0-1.25.5-2.4 1-3.44 0 0-1.89-6.42-.5-7 1.39-.58 4.72.23 6.5 2.23A9.04 9.04 0 0 1 12 5Z\" /><path d=\"M8 14v.5\" /><path d=\"M16 14v.5\" /><path d=\"M11.25 16.25h1.5L12 17l-.75-.75Z\" />", "stethoscope": "<path d=\"M11 2v2\" /><path d=\"M5 2v2\" /><path d=\"M5 3H4a2 2 0 0 0-2 2v4a6 6 0 0 0 12 0V5a2 2 0 0 0-2-2h-1\" /><path d=\"M8 15a6 6 0 0 0 12 0v-3\" /><circle cx=\"20\" cy=\"10\" r=\"2\" />", "heart": "<path d=\"M2 9.5a5.5 5.5 0 0 1 9.591-3.676.56.56 0 0 0 .818 0A5.49 5.49 0 0 1 22 9.5c0 2.29-1.5 4-3 5.5l-5.492 5.313a2 2 0 0 1-3 .019L5 15c-1.5-1.5-3-3.2-3-5.5\" />", "bone": "<path d=\"M17 10c.7-.7 1.69 0 2.5 0a2.5 2.5 0 1 0 0-5 .5.5 0 0 1-.5-.5 2.5 2.5 0 1 0-5 0c0 .81.7 1.8 0 2.5l-7 7c-.7.7-1.69 0-2.5 0a2.5 2.5 0 0 0 0 5c.28 0 .5.22.5.5a2.5 2.5 0 1 0 5 0c0-.81-.7-1.8 0-2.5Z\" />", "shield-check": "<path d=\"M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z\" /><path d=\"m9 12 2 2 4-4\" />", "book-open": "<path d=\"M12 5v16\" /><path d=\"M20.001 19A2 2 0 0022 17V5a2 2 0 00-1.999-2L16 3.002A5 5 0 0012 5a5 5 0 00-4-2H4a2 2 0 00-2 2v12a2 2 0 001.999 2H8a5 5 0 014 2 5 5 0 014-2z\" />", "sun": "<circle cx=\"12\" cy=\"12\" r=\"4\" /><path d=\"M12 2v2\" /><path d=\"M12 20v2\" /><path d=\"m4.93 4.93 1.41 1.41\" /><path d=\"m17.66 17.66 1.41 1.41\" /><path d=\"M2 12h2\" /><path d=\"M20 12h2\" /><path d=\"m6.34 17.66-1.41 1.41\" /><path d=\"m19.07 4.93-1.41 1.41\" />", "moon": "<path d=\"M20.985 12.486a9 9 0 1 1-9.473-9.472c.405-.022.617.46.402.803a6 6 0 0 0 8.268 8.268c.344-.215.825-.004.803.401\" />", "house": "<path d=\"M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8\" /><path d=\"M3 10a2 2 0 0 1 .709-1.528l7-6a2 2 0 0 1 2.582 0l7 6A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z\" />", "layers": "<path d=\"M12.83 2.18a2 2 0 0 0-1.66 0L2.6 6.08a1 1 0 0 0 0 1.83l8.58 3.91a2 2 0 0 0 1.66 0l8.58-3.9a1 1 0 0 0 0-1.83z\" /><path d=\"M2 12a1 1 0 0 0 .58.91l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9A1 1 0 0 0 22 12\" /><path d=\"M2 17a1 1 0 0 0 .58.91l8.6 3.91a2 2 0 0 0 1.65 0l8.58-3.9A1 1 0 0 0 22 17\" />", "circle-help": "<circle cx=\"12\" cy=\"12\" r=\"10\" /><path d=\"M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3\" /><path d=\"M12 17h.01\" />", "mail": "<path d=\"m22 7-8.991 5.727a2 2 0 0 1-2.009 0L2 7\" /><rect x=\"2\" y=\"4\" width=\"20\" height=\"16\" rx=\"2\" />", "scale": "<path d=\"M12 3v18\" /><path d=\"m19 8 3 8a5 5 0 0 1-6 0zV7\" /><path d=\"M3 7h1a17 17 0 0 0 8-2 17 17 0 0 0 8 2h1\" /><path d=\"m5 8 3 8a5 5 0 0 1-6 0zV7\" /><path d=\"M7 21h10\" />", "receipt": "<path d=\"M12 17V7\" /><path d=\"M16 8h-6a2 2 0 0 0 0 4h4a2 2 0 0 1 0 4H8\" /><path d=\"M4 3a1 1 0 0 1 1-1 1.3 1.3 0 0 1 .7.2l.933.6a1.3 1.3 0 0 0 1.4 0l.934-.6a1.3 1.3 0 0 1 1.4 0l.933.6a1.3 1.3 0 0 0 1.4 0l.933-.6a1.3 1.3 0 0 1 1.4 0l.934.6a1.3 1.3 0 0 0 1.4 0l.933-.6A1.3 1.3 0 0 1 19 2a1 1 0 0 1 1 1v18a1 1 0 0 1-1 1 1.3 1.3 0 0 1-.7-.2l-.933-.6a1.3 1.3 0 0 0-1.4 0l-.934.6a1.3 1.3 0 0 1-1.4 0l-.933-.6a1.3 1.3 0 0 0-1.4 0l-.933.6a1.3 1.3 0 0 1-1.4 0l-.934-.6a1.3 1.3 0 0 0-1.4 0l-.933.6a1.3 1.3 0 0 1-.7.2 1 1 0 0 1-1-1z\" />", "sparkle": "<path d=\"M11.017 2.814a1 1 0 0 1 1.966 0l1.051 5.558a2 2 0 0 0 1.594 1.594l5.558 1.051a1 1 0 0 1 0 1.966l-5.558 1.051a2 2 0 0 0-1.594 1.594l-1.051 5.558a1 1 0 0 1-1.966 0l-1.051-5.558a2 2 0 0 0-1.594-1.594l-5.558-1.051a1 1 0 0 1 0-1.966l5.558-1.051a2 2 0 0 0 1.594-1.594z\" />", "smartphone": "<rect width=\"14\" height=\"20\" x=\"5\" y=\"2\" rx=\"2\" ry=\"2\" /><path d=\"M12 18h.01\" />", "monitor": "<rect width=\"20\" height=\"14\" x=\"2\" y=\"3\" rx=\"2\" /><line x1=\"8\" x2=\"16\" y1=\"21\" y2=\"21\" /><line x1=\"12\" x2=\"12\" y1=\"17\" y2=\"21\" />", "gamepad-2": "<line x1=\"6\" x2=\"10\" y1=\"11\" y2=\"11\" /><line x1=\"8\" x2=\"8\" y1=\"9\" y2=\"13\" /><line x1=\"15\" x2=\"15.01\" y1=\"12\" y2=\"12\" /><line x1=\"18\" x2=\"18.01\" y1=\"10\" y2=\"10\" /><path d=\"M17.32 5H6.68a4 4 0 0 0-3.978 3.59c-.006.052-.01.101-.017.152C2.604 9.416 2 14.456 2 16a3 3 0 0 0 3 3c1 0 1.5-.5 2-1l1.414-1.414A2 2 0 0 1 9.828 16h4.344a2 2 0 0 1 1.414.586L17 18c.5.5 1 1 2 1a3 3 0 0 0 3-3c0-1.545-.604-6.584-.685-7.258-.007-.05-.011-.1-.017-.151A4 4 0 0 0 17.32 5z\" />", "globe": "<circle cx=\"12\" cy=\"12\" r=\"10\" /><path d=\"M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20\" /><path d=\"M2 12h20\" />", "message-circle": "<path d=\"M2.992 16.342a2 2 0 0 1 .094 1.167l-1.065 3.29a1 1 0 0 0 1.236 1.168l3.413-.998a2 2 0 0 1 1.099.092 10 10 0 1 0-4.777-4.719\" />", "cloud": "<path d=\"M17.5 19H9a7 7 0 1 1 6.71-9h1.79a4.5 4.5 0 1 1 0 9Z\" />", "credit-card": "<rect width=\"20\" height=\"14\" x=\"2\" y=\"5\" rx=\"2\" /><line x1=\"2\" x2=\"22\" y1=\"10\" y2=\"10\" /><path d=\"M6 14h2\" />", "user": "<path d=\"M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2\" /><circle cx=\"12\" cy=\"7\" r=\"4\" />", "ban": "<circle cx=\"12\" cy=\"12\" r=\"10\" /><path d=\"M4.929 4.929 19.07 19.071\" />", "refresh-cw": "<path d=\"M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8\" /><path d=\"M21 3v5h-5\" /><path d=\"M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16\" /><path d=\"M8 16H3v5\" />", "lightbulb": "<path d=\"M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5\" /><path d=\"M9 18h6\" /><path d=\"M10 22h4\" />", "flask-conical": "<path d=\"M14 2v6a2 2 0 0 0 .245.96l5.51 10.08A2 2 0 0 1 18 22H6a2 2 0 0 1-1.755-2.96l5.51-10.08A2 2 0 0 0 10 8V2\" /><path d=\"M6.453 15h11.094\" /><path d=\"M8.5 2h7\" />", "utensils": "<path d=\"M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2\" /><path d=\"M7 2v20\" /><path d=\"M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7\" />", "pill": "<path d=\"m10.5 20.5 10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7Z\" /><path d=\"m8.5 8.5 7 7\" />", "syringe": "<path d=\"m18 2 4 4\" /><path d=\"m17 7 3-3\" /><path d=\"M19 9 8.7 19.3c-1 1-2.5 1-3.4 0l-.6-.6c-1-1-1-2.5 0-3.4L15 5\" /><path d=\"m9 11 4 4\" /><path d=\"m5 19-3 3\" /><path d=\"m14 4 6 6\" />", "bug": "<path d=\"M12 20v-9\" /><path d=\"M14 7a4 4 0 0 1 4 4v3a6 6 0 0 1-12 0v-3a4 4 0 0 1 4-4z\" /><path d=\"M14.12 3.88 16 2\" /><path d=\"M21 21a4 4 0 0 0-3.81-4\" /><path d=\"M21 5a4 4 0 0 1-3.55 3.97\" /><path d=\"M22 13h-4\" /><path d=\"M3 21a4 4 0 0 1 3.81-4\" /><path d=\"M3 5a4 4 0 0 0 3.55 3.97\" /><path d=\"M6 13H2\" /><path d=\"m8 2 1.88 1.88\" /><path d=\"M9 7.13V6a3 3 0 1 1 6 0v1.13\" />", "thermometer": "<path d=\"M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z\" />", "siren": "<path d=\"M7 18v-6a5 5 0 1 1 10 0v6\" /><path d=\"M5 21a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1v-1a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2z\" /><path d=\"M21 12h1\" /><path d=\"M18.5 4.5 18 5\" /><path d=\"M2 12h1\" /><path d=\"M12 2v1\" /><path d=\"m4.929 4.929.707.707\" /><path d=\"M12 12v6\" />", "list": "<path d=\"M3 5h.01\" /><path d=\"M3 12h.01\" /><path d=\"M3 19h.01\" /><path d=\"M8 5h13\" /><path d=\"M8 12h13\" /><path d=\"M8 19h13\" />", "home": "<path d=\"M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8\" /><path d=\"M3 10a2 2 0 0 1 .709-1.528l7-6a2 2 0 0 1 2.582 0l7 6A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z\" />", "brush-cleaning": "<path d=\"m16 22-1-4\" /><path d=\"M19 14a1 1 0 0 0 1-1v-1a2 2 0 0 0-2-2h-3a1 1 0 0 1-1-1V4a2 2 0 0 0-4 0v5a1 1 0 0 1-1 1H6a2 2 0 0 0-2 2v1a1 1 0 0 0 1 1\" /><path d=\"M19 14H5l-1.973 6.767A1 1 0 0 0 4 22h16a1 1 0 0 0 .973-1.233z\" /><path d=\"m8 22 1-4\" />", "building-2": "<path d=\"M10 12h4\" /><path d=\"M10 8h4\" /><path d=\"M14 21v-3a2 2 0 0 0-4 0v3\" /><path d=\"M6 10H4a2 2 0 0 0-2 2v7a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-2\" /><path d=\"M6 21V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v16\" />", "leaf": "<path d=\"M11 20a10 10 0 0010-10 25.9 25.9 0 00-1.04-7.281 1 1 0 00-1.755-.325C15.833 5.5 13 5.5 9.8 6.1A7 7 0 0011 20\" /><path d=\"M2 21a5 5 0 012.911-4.544C7.613 15.212 8.351 15.24 11 13\" />", "apple": "<path d=\"M12 6.528V3a1 1 0 0 1 1-1h0\" /><path d=\"M18.237 21A15 15 0 0 0 22 11a6 6 0 0 0-10-4.472A6 6 0 0 0 2 11a15.1 15.1 0 0 0 3.763 10 3 3 0 0 0 3.648.648 5.5 5.5 0 0 1 5.178 0A3 3 0 0 0 18.237 21\" />", "bath": "<path d=\"M10 4 8 6\" /><path d=\"M17 19v2\" /><path d=\"M2 12h20\" /><path d=\"M7 19v2\" /><path d=\"M9 5 7.621 3.621A2.121 2.121 0 0 0 4 5v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-5\" />", "scissors": "<circle cx=\"6\" cy=\"6\" r=\"3\" /><path d=\"M8.12 8.12 12 12\" /><path d=\"M20 4 8.12 15.88\" /><circle cx=\"6\" cy=\"18\" r=\"3\" /><path d=\"M14.8 14.8 20 20\" />", "users": "<path d=\"M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2\" /><path d=\"M16 3.128a4 4 0 0 1 0 7.744\" /><path d=\"M22 21v-2a4 4 0 0 0-3-3.87\" /><circle cx=\"9\" cy=\"7\" r=\"4\" />"}
CREDIT = 'Icons from <a href="https://lucide.dev" rel="nofollow">Lucide</a> (ISC/MIT license). Service logos via Google favicon service, trademarks of their owners.'

def icon(name, size=20, cls="ic", label=None):
    body = ICONS.get(name) or ICONS["circle-help"]
    a = f'role="img" aria-label="{_h.escape(label)}"' if label else 'aria-hidden="true" focusable="false"'
    return (f'<svg class="{cls}" {a} width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{body}</svg>')

def flogo(domain, alt, size=32, lazy=True, cls="flogo"):
    d = re.sub(r"^https?://", "", domain).split("/")[0].replace("www.", "")
    return (f'<img class="{cls}" src="https://www.google.com/s2/favicons?domain={d}&amp;sz=64" alt="{_h.escape(alt)} logo" '
            f'width="{size}" height="{size}"{" loading=\"lazy\"" if lazy else ""} decoding="async">')

THEME_HEAD = ("<script>(function(){try{var s=localStorage.getItem('theme'),h=new Date().getHours();"
              "document.documentElement.setAttribute('data-theme',s||((h>=19||h<7)?'dark':'light'))}catch(e){}})()</script>")

def toggle():
    return ('<button class="thm" type="button" aria-label="Switch light or dark mode" title="Switch light or dark mode" '
            "onclick=\"var d=document.documentElement,t=d.getAttribute('data-theme')=='dark'?'light':'dark';"
            "d.setAttribute('data-theme',t);try{localStorage.setItem('theme',t)}catch(e){}\">"
            + icon("moon", 18, "ic i-moon") + icon("sun", 18, "ic i-sun") + "</button>")

GFX_CSS = """
.ic{display:inline-block;vertical-align:-.18em;flex:none}
nav a .ic{width:16px;height:16px;margin-right:5px;opacity:.75}
.thm{display:inline-grid;place-items:center;width:36px;height:36px;border-radius:10px;border:1px solid var(--gx-bd,#e5e7eb);background:transparent;color:inherit;cursor:pointer;margin-left:14px;flex:none;padding:0}
.thm:hover{background:rgba(127,127,127,.12)}.thm .i-sun{display:none}
html[data-theme=dark] .thm .i-sun{display:block}html[data-theme=dark] .thm .i-moon{display:none}
.flogo{border-radius:8px;background:#fff;object-fit:contain;flex:none;vertical-align:middle}
.ibadge{display:inline-grid;place-items:center;width:44px;height:44px;border-radius:13px;background:var(--c,#4f46e5);color:#fff;flex:none;box-shadow:inset 0 -3px 0 rgba(0,0,0,.12)}
.ibadge.sm{width:34px;height:34px;border-radius:10px}.ibadge.lg{width:64px;height:64px;border-radius:18px}
.ibadge.soft{background:color-mix(in srgb,var(--c) 13%,transparent);color:var(--c);box-shadow:none}
.gchip{display:inline-flex;align-items:center;gap:5px}
.hero-gfx{display:block;width:100%;height:auto;max-width:520px;margin:0 auto}
.gx-soft{fill:#f3f5f9}.gx-card{fill:#fff;stroke:#e5e7eb}.gx-line{fill:#e5e7eb}
html[data-theme=dark] .gx-soft{fill:#1a1e26}html[data-theme=dark] .gx-card{fill:#161a21;stroke:#2c3240}html[data-theme=dark] .gx-line{fill:#2c3240}
.secdeco{display:flex;align-items:center;gap:10px}.secdeco .ibadge{width:36px;height:36px;border-radius:11px}
html[data-theme=dark]{color-scheme:dark}
html[data-theme=dark] header img[src*="wordmark"],html[data-theme=dark] footer img[src*="wordmark"],html[data-theme=dark] .top img[src*="wordmark"],html[data-theme=dark] .foot img[src*="wordmark"]{background:#fff;border-radius:9px;padding:4px 8px;box-sizing:content-box}
html[data-theme=dark] img:not(.flogo):not([src*=".svg"]){filter:brightness(.92)}
"""

# ---------- dark mode CSS derived from the light stylesheet ----------
_CP = re.compile(r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\)|\bwhite\b")
def _parse(c):
    if c == "white": return 255, 255, 255, 1
    if c.startswith("#"):
        h = c[1:]
        if len(h) in (3, 4): h = "".join(x * 2 for x in h)
        a = int(h[6:8], 16) / 255 if len(h) == 8 else 1
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), a
    p = [x.strip() for x in c[c.index("(") + 1:-1].replace("/", ",").split(",") if x.strip()]
    return int(float(p[0])), int(float(p[1])), int(float(p[2])), float(p[3]) if len(p) > 3 else 1

def _fmt(r, g, b, a):
    return f"#{r:02x}{g:02x}{b:02x}" if a >= 1 else f"rgba({r},{g},{b},{round(a,3)})"

def _map(c, prop):
    r, g, b, a = _parse(c)
    h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    neutral = s < .18 or l > .96 or l < .06
    if prop == "color" and l > .85: return c          # light text on colored fills stays
    if neutral:
        if prop.startswith("background") and l < .3: L = .16
        elif l >= .5: L = .07 + (1 - l) * .9
        else: L = 1 - l * .75
        h, s = .6, .12
    else:
        if l > .85: L, s = .14 + (1 - l) * .6, min(s, .45)
        elif l < .25: L = .16 if prop.startswith("background") else .85
        elif l < .42 and not prop.startswith("background"): L = .66
        else: L = l
    if c in ("#fff", "#ffffff", "white") or (r, g, b) == (255, 255, 255): R, G, B = 15, 17, 21
    else: R, G, B = (int(round(x * 255)) for x in colorsys.hls_to_rgb(h, L, s))
    return _fmt(R, G, B, a)

_PROPS = ("color", "background", "border", "box-shadow", "outline", "fill", "stroke", "text-decoration", "--", "caret", "accent")
def _sel(s):
    s = s.strip()
    if s.startswith(":root") or s == "html": return "html[data-theme=dark]" + s.replace(":root", "").replace("html", "", 1)
    if s.startswith("html"): return "html[data-theme=dark]" + s[4:]
    return "html[data-theme=dark] " + s

def _walk(css):
    out, i = [], 0
    for m in re.finditer(r"([^{}]+)\{((?:[^{}]|\{[^{}]*\})*)\}", css):
        sel, body = m.group(1).strip(), m.group(2)
        if sel.startswith("@keyframes") or sel.startswith("@font-face") or sel.startswith("@import"): continue
        if sel.startswith("@media") or sel.startswith("@supports"):
            inner = _walk(body)
            if inner: out.append(sel + "{" + inner + "}")
            continue
        decl = []
        for d in body.split(";"):
            if ":" not in d: continue
            p, v = d.split(":", 1); p = p.strip().lower()
            if not p.startswith(_PROPS) or "url(" in v: continue
            nv = _CP.sub(lambda mm: _map(mm.group(0), "color" if p == "color" else p), v)
            if nv != v: decl.append(f"{p}:{nv.strip()}")
        if decl and "data-theme" not in sel:
            out.append(",".join(_sel(x) for x in sel.split(",")) + "{" + ";".join(decl) + "}")
    return "".join(out)

M1, M2 = "/* gfx:start (generated by atulit_gfx.py) */", "/* gfx:end */"
def install_css(path, extra=""):
    css = open(path).read()
    if M1 in css: css = css[:css.index(M1)].rstrip() + css[css.index(M2) + len(M2):]
    base = css.rstrip() + "\n" + extra
    dark = _walk(re.sub(r"/\*.*?\*/", "", base, flags=re.S))
    dark += "html[data-theme=dark],html[data-theme=dark] body{background:#0f1115;color:#e6e8ec}html[data-theme=dark] .ibadge.soft{background:color-mix(in srgb,var(--c) 22%,transparent)}"
    open(path, "w").write(css.rstrip() + "\n" + M1 + GFX_CSS + extra + "\n" + dark + "\n" + M2 + "\n")

# ---------- hero illustrations (inline SVG, brand colors) ----------
def _svg(inner, label):
    return f'<svg class="hero-gfx" viewBox="0 0 480 360" width="480" height="360" role="img" aria-label="{_h.escape(label)}" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'

def _ic(name, x, y, s, color):
    return f'<g transform="translate({x} {y}) scale({s/24})" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>'

def hero(kind):
    if kind == "trialtally":
        a, b, k = "#FF5A36", "#FFC531", "#2B1A12"
        g = (f'<circle class="gx-soft" cx="250" cy="185" r="160"/><circle cx="400" cy="70" r="26" fill="{b}" opacity=".9"/><circle cx="70" cy="290" r="14" fill="{a}" opacity=".35"/>'
             f'<rect class="gx-card" x="100" y="70" width="230" height="220" rx="22" stroke-width="2"/><rect x="100" y="70" width="230" height="52" rx="22" fill="{a}"/><rect x="100" y="100" width="230" height="22" fill="{a}"/>'
             f'<rect x="140" y="56" width="10" height="34" rx="5" fill="{k}"/><rect x="280" y="56" width="10" height="34" rx="5" fill="{k}"/>')
        days = ""
        for i in range(15):
            cx, cy = 128 + (i % 5) * 44, 148 + (i // 5) * 44
            if i in (0, 1, 2, 3, 4, 5, 6): days += f'<circle cx="{cx+8}" cy="{cy+8}" r="15" fill="{b}" opacity=".25"/>' + _ic("circle-check", cx - 3, cy - 3, 22, a)
            elif i == 13: days += f'<circle cx="{cx+8}" cy="{cy+8}" r="16" fill="{k}"/>' + _ic("calendar-x", cx, cy, 16, "#fff")
            else: days += f'<rect class="gx-line" x="{cx-4}" y="{cy-4}" width="24" height="24" rx="7"/>'
        tag = (f'<g transform="translate(300 200) rotate(-12)"><path d="M0 0h110l26 30-26 30H0z" fill="{b}"/><circle cx="112" cy="30" r="6" fill="#fff"/>'
               f'{_ic("dollar-sign", 16, 14, 32, k)}<rect x="52" y="22" width="44" height="7" rx="3.5" fill="{k}" opacity=".7"/><rect x="52" y="34" width="30" height="7" rx="3.5" fill="{k}" opacity=".35"/></g>')
        clock = f'<circle cx="92" cy="96" r="34" fill="{k}"/>' + _ic("clock", 70, 74, 44, b)
        return _svg(g + days + tag + clock, "Illustration of a free trial calendar with checked days, a price tag and a clock")
    if kind == "downfixer":
        n, t, m = "#0E2A3F", "#0F9D8A", "#2DD4A7"
        g = (f'<circle class="gx-soft" cx="240" cy="180" r="165"/><circle cx="410" cy="300" r="20" fill="{m}" opacity=".5"/><circle cx="64" cy="70" r="12" fill="{t}" opacity=".4"/>'
             f'<rect x="70" y="70" width="270" height="180" rx="18" fill="{n}"/><rect x="84" y="84" width="242" height="140" rx="10" fill="#12354f"/>'
             f'<polyline points="96,160 140,160 158,120 182,200 204,140 220,160 314,160" fill="none" stroke="{m}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
             f'<rect x="180" y="250" width="50" height="26" fill="{n}"/><rect x="146" y="272" width="118" height="12" rx="6" fill="{n}"/>'
             f'<circle cx="100" cy="100" r="5" fill="#ef4444"/><circle cx="116" cy="100" r="5" fill="#f59e0b"/><circle cx="132" cy="100" r="5" fill="{m}"/>')
        srv = ""
        for i, c in enumerate([m, m, "#f59e0b"]):
            y = 120 + i * 50
            srv += f'<rect class="gx-card" x="320" y="{y}" width="120" height="40" rx="10" stroke-width="2"/><circle cx="342" cy="{y+20}" r="7" fill="{c}"/><rect class="gx-line" x="358" y="{y+16}" width="64" height="8" rx="4"/>'
        wr = f'<circle cx="370" cy="74" r="32" fill="{t}"/>' + _ic("wrench", 352, 56, 36, "#fff")
        ok = f'<circle cx="94" cy="262" r="26" fill="{m}"/>' + _ic("circle-check", 78, 246, 32, n)
        return _svg(g + srv + wr + ok, "Illustration of a status monitor with a live pulse line, server lights and a repair wrench")
    if kind == "aiforthetask":
        a, b, k = "#4F46E5", "#06B6D4", "#1E1B4B"
        defs = f'<defs><linearGradient id="gxg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient></defs>'
        g = (f'<circle class="gx-soft" cx="240" cy="180" r="165"/><circle cx="420" cy="70" r="16" fill="{b}" opacity=".5"/><circle cx="60" cy="300" r="22" fill="{a}" opacity=".18"/>'
             f'<rect class="gx-card" x="80" y="60" width="300" height="230" rx="20" stroke-width="2"/><rect x="80" y="60" width="300" height="38" rx="20" fill="url(#gxg)"/><rect x="80" y="80" width="300" height="18" fill="url(#gxg)"/>'
             f'<circle cx="102" cy="79" r="5" fill="#fff" opacity=".8"/><circle cx="118" cy="79" r="5" fill="#fff" opacity=".6"/><circle cx="134" cy="79" r="5" fill="#fff" opacity=".4"/>')
        tiles = ""
        for i, (nm, c) in enumerate([("file-user", "#6366f1"), ("image", "#a855f7"), ("code", "#14b8a6"), ("mic", "#ef4444"), ("presentation", "#eab308"), ("pencil-line", "#0ea5e9")]):
            x, y = 104 + (i % 3) * 88, 118 + (i // 3) * 82
            tiles += f'<rect x="{x}" y="{y}" width="72" height="66" rx="14" fill="{c}" opacity=".14"/>' + _ic(nm, x + 22, y + 12, 28, c) + f'<rect class="gx-line" x="{x+14}" y="{y+48}" width="44" height="6" rx="3"/>'
        sp = f'<circle cx="378" cy="250" r="44" fill="url(#gxg)"/>' + _ic("sparkles", 352, 224, 52, "#fff")
        return _svg(defs + g + tiles + sp, "Illustration of an app window with AI task tiles for resumes, images, coding, voice, slides and writing")
    if kind == "cityratebook":
        gr, go = "#14532D", "#D9A21B"
        g = f'<circle class="gx-soft" cx="240" cy="190" r="160"/><circle cx="410" cy="70" r="24" fill="{go}" opacity=".85"/>'
        bld = ""
        for x, w, h in [(70, 46, 120), (122, 40, 170), (168, 56, 100), (300, 44, 150), (350, 52, 110), (408, 36, 80)]:
            bld += f'<rect x="{x}" y="{290-h}" width="{w}" height="{h}" rx="6" fill="{gr}" opacity=".85"/>'
            for yy in range(290 - h + 14, 280, 22):
                bld += f'<rect x="{x+9}" y="{yy}" width="{w-18}" height="7" rx="2" fill="{go}" opacity=".55"/>'
        house = (f'<path d="M206 200 L262 152 L318 200 V290 H206 Z" class="gx-card" stroke-width="3"/><path d="M196 206 L262 148 L328 206" fill="none" stroke="{gr}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
                 f'<rect x="246" y="240" width="32" height="50" rx="4" fill="{go}"/>')
        tag = f'<g transform="translate(330 168) rotate(10)"><path d="M0 0h86l22 24-22 24H0z" fill="{go}"/><circle cx="88" cy="24" r="5" fill="#fff"/>' + _ic("dollar-sign", 12, 10, 28, gr) + f'<rect x="44" y="18" width="30" height="7" rx="3.5" fill="{gr}" opacity=".6"/></g>'
        pin = f'<circle cx="112" cy="90" r="30" fill="{gr}"/>' + _ic("map-pin", 94, 72, 36, go)
        tools = f'<circle cx="262" cy="104" r="24" fill="{go}"/>' + _ic("wrench", 249, 91, 26, gr)
        base = f'<rect x="50" y="288" width="400" height="8" rx="4" fill="{gr}" opacity=".25"/>'
        return _svg(g + bld + base + house + tag + pin + tools, "Illustration of a city skyline with a house, a price tag, a map pin and a wrench")
    raise KeyError(kind)
