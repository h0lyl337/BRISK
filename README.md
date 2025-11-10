This repository contains a small Flask application that issues single-use URLs. When a link is visited the server and client-side JavaScript attempt to capture available browser metadata (for example: IP address, browser/OS hints, locale/keyboard information, display frame/refresh metrics, and other non-invasive client-side metrics). After the URL is used once it becomes invalid, ensuring only the intended click is recorded.

Use cases

Authorized penetration testing and red-team exercises

Usability and client-metrics research (with consent)

Key features

Single-use URL issuance and server-side invalidation after first access

Client-side JavaScript hooks to collect browser-provided metrics

Server-side logging of request metadata (timestamp, IP, user-agent, etc.)

Extensible design for adding more benign diagnostics over time

Security & Ethics
This project is intended only for lawful, ethical use. Do not deploy or use this tool to track, identify, or otherwise monitor individuals without their explicit, informed consent and any required legal authorization. Collecting or attempting to infer sensitive data (precise location, personal identifiers) can violate privacy laws and platform rules. Before using this tool in any environment:

Obtain written consent from the people you are testing.

Comply with applicable laws (privacy, wiretapping, data protection).
