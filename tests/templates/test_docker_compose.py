#!/usr/bin/env python3
"""
Test the docker-compose.yml.j2 Jinja2 template rendering.

The template generates a Docker Compose service definition with two conditional
blocks:
  - Java: JAVA_HOME env var and a bind-mount volume (when splunk_docker_java_enabled)
  - SSL:  healthcheck URL uses https vs http (based on splunk_docker_web_ssl)

Run from repo root:
  python3 tests/templates/test_docker_compose.py
"""

import sys
from pathlib import Path

try:
    from jinja2 import Environment, FileSystemLoader
except ImportError:
    print("ERROR: jinja2 not installed. Run: pip install jinja2")
    sys.exit(1)

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml")
    sys.exit(1)

TEMPLATE_DIR = Path(__file__).parent.parent.parent / "roles/splunk_docker/templates"
env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)), keep_trailing_newline=True)
template = env.get_template("docker-compose.yml.j2")

errors = []

# Shared base vars (Java disabled, SSL enabled — the production defaults)
BASE_VARS = {
    "splunk_docker_image": "splunk/splunk:latest",
    "splunk_docker_hostname": "splunk",
    "splunk_docker_container_name": "splunk",
    "splunk_docker_password": "Ch@ngeMe123",
    "splunk_docker_hec_token_values": {"legacy": "aaaaaaaa-0000-5000-8000-aaaaaaaaaaaa"},
    "splunk_docker_web_port": 8000,
    "splunk_docker_mgmt_port": 8089,
    "splunk_docker_mgmt_bind": "0.0.0.0",
    "splunk_docker_hec_port": 8088,
    "splunk_docker_var_dir": "/opt/splunk/var",
    "splunk_docker_etc_dir": "/opt/splunk/etc",
    "splunk_docker_java_enabled": False,
    "splunk_docker_java_home": "/usr/lib/jvm/temurin-21-jre-amd64",
    "splunk_docker_java_container_home": "/opt/java",
    "splunk_docker_web_ssl": True,
}

result_default = template.render(**BASE_VARS)

# Test 1: Output is valid YAML
try:
    parsed = yaml.safe_load(result_default)
    print("PASS: rendered output is valid YAML")
except yaml.YAMLError as exc:
    errors.append(f"FAIL: rendered output is not valid YAML: {exc}")
    parsed = None

# Test 2: Core service fields are present
if parsed is not None:
    svc = parsed.get("services", {}).get("splunk", {})
    if not svc:
        errors.append("FAIL: 'services.splunk' missing from parsed YAML")
    else:
        if svc.get("image") != BASE_VARS["splunk_docker_image"]:
            errors.append(f"FAIL: image field wrong: {svc.get('image')!r}")
        elif svc.get("hostname") != BASE_VARS["splunk_docker_hostname"]:
            errors.append(f"FAIL: hostname field wrong: {svc.get('hostname')!r}")
        else:
            print("PASS: core service fields (image, hostname) are correct")

# Test 3: Java disabled → no JAVA_HOME env var, no java volume mount
if "JAVA_HOME" in result_default:
    errors.append("FAIL: JAVA_HOME present in output when java is disabled")
elif BASE_VARS["splunk_docker_java_home"] in result_default:
    errors.append("FAIL: java host path present in volumes when java is disabled")
else:
    print("PASS: java disabled → no JAVA_HOME or java volume in output")

# Test 4: Java enabled → JAVA_HOME env var and java volume mount are present
java_vars = {**BASE_VARS, "splunk_docker_java_enabled": True}
result_java = template.render(**java_vars)
if "JAVA_HOME" not in result_java:
    errors.append("FAIL: JAVA_HOME missing when java is enabled")
elif BASE_VARS["splunk_docker_java_home"] not in result_java:
    errors.append("FAIL: java host volume path missing when java is enabled")
elif BASE_VARS["splunk_docker_java_container_home"] not in result_java:
    errors.append("FAIL: java container mount path missing when java is enabled")
else:
    print("PASS: java enabled → JAVA_HOME env var and java volume mount present")

# Test 5: SSL enabled → healthcheck uses https://
if "https://localhost:8000" not in result_default:
    errors.append("FAIL: healthcheck does not use https when splunk_docker_web_ssl=true")
else:
    print("PASS: SSL enabled → healthcheck URL uses https")

# Test 6: SSL disabled → healthcheck uses http://
no_ssl_vars = {**BASE_VARS, "splunk_docker_web_ssl": False}
result_no_ssl = template.render(**no_ssl_vars)
if "http://localhost:8000" not in result_no_ssl:
    errors.append("FAIL: healthcheck does not use http when splunk_docker_web_ssl=false")
elif "https://localhost:8000" in result_no_ssl:
    errors.append("FAIL: healthcheck still uses https when splunk_docker_web_ssl=false")
else:
    print("PASS: SSL disabled → healthcheck URL uses http")

if errors:
    print()
    for err in errors:
        print(err)
    sys.exit(1)

print("\nAll tests passed.")
