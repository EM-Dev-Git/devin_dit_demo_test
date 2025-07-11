#!/usr/bin/env python3

print("Testing Microsoft Graph integration imports...")

try:
    from modules.graph_client import graph_client
    print("✓ Graph client imports successful")
except Exception as e:
    print(f"✗ Graph client imports failed: {e}")

try:
    from schemas.graph import GraphMeetingListRequest, GraphTranscriptImportRequest
    print("✓ Graph schema imports successful")
except Exception as e:
    print(f"✗ Graph schema imports failed: {e}")

try:
    from routers.graph import router
    print("✓ Graph router imports successful")
except Exception as e:
    print(f"✗ Graph router imports failed: {e}")

try:
    from main import app
    print("✓ Main app with Graph integration imports successful")
except Exception as e:
    print(f"✗ Main app imports failed: {e}")

print("Microsoft Graph integration import testing complete!")
