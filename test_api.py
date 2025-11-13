import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def print_response(label, response):
    """Helper function to print responses consistently"""
    print(f"\n{label}")
    print(f"Status: {response.status_code}")
    try:
        if response.text:
            print("Response:")
            print(json.dumps(response.json(), indent=2))
        else:
            print("Response: (empty)")
    except json.JSONDecodeError:
        print(f"Response (raw): {response.text}")

def test_endpoints():
    print("=== Maisha Uni Backend API Testing ===")
    print("Make sure the server is running on localhost:8000\n")
    
    # Store tokens for reuse
    tokens = {}
    
    # 1. Test Registration
    print("1. TESTING USER REGISTRATION")
    print("-" * 40)
    
    # Register student
    student_data = {
        "email": "teststudent@example.com",
        "full_name": "Test Student",
        "role": "student",
        "password": "testpass123",
        "password2": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/register/", json=student_data)
    print_response("Student Registration", response)
    
    if response.status_code == 201:
        student_tokens = response.json()
        tokens['student'] = student_tokens['access']
        print("✓ Student tokens stored")
    else:
        print("✗ Cannot continue without student registration")
        return
    
    # Register admin
    admin_data = {
        "email": "testadmin@example.com",
        "full_name": "Test Admin",
        "role": "admin",
        "password": "testpass123",
        "password2": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/register/", json=admin_data)
    print_response("Admin Registration", response)
    
    if response.status_code == 201:
        admin_tokens = response.json()
        tokens['admin'] = admin_tokens['access']
        print("✓ Admin tokens stored")
    else:
        print("✗ Cannot continue without admin registration")
        return
    
    # 2. Test Login
    print("\n2. TESTING USER LOGIN")
    print("-" * 40)
    
    login_data = {
        "email": "teststudent@example.com",
        "password": "testpass123"
    }
    
    response = requests.post(f"{BASE_URL}/api/auth/login/", json=login_data)
    print_response("Student Login", response)
    
    if response.status_code == 200:
        print("✓ Login successful")
    else:
        print("✗ Login failed")
    
    # 3. Test Profile Endpoints
    print("\n3. TESTING PROFILE ENDPOINTS")
    print("-" * 40)
    
    student_headers = {"Authorization": f"Bearer {tokens['student']}"}
    
    # Get profile
    response = requests.get(f"{BASE_URL}/api/auth/profile/", headers=student_headers)
    print_response("Get Student Profile", response)
    
    if response.status_code == 200:
        profile_data = response.json()
        print(f"✓ Profile retrieved - ID: {profile_data['id']}")
    
    # Update profile
    update_data = {
        "university": "University of Nairobi",
        "course": "Computer Science",
        "year": "3rd Year",
        "bio": "Passionate about software development and AI technologies. Looking for internship opportunities."
    }
    
    response = requests.put(f"{BASE_URL}/api/auth/profile/", json=update_data, headers=student_headers)
    print_response("Update Student Profile", response)
    
    if response.status_code == 200:
        print("✓ Profile updated successfully")
    
    # 4. Test Announcements Endpoints
    print("\n4. TESTING ANNOUNCEMENTS ENDPOINTS")
    print("-" * 40)
    
    # Get announcements (student)
    response = requests.get(f"{BASE_URL}/api/announcements/", headers=student_headers)
    print_response("Get Announcements (Student)", response)
    
    if response.status_code == 200:
        announcements = response.json()
        print(f"✓ Retrieved {len(announcements)} announcements")
    
    # Create announcement as admin
    admin_headers = {"Authorization": f"Bearer {tokens['admin']}"}
    announcement_data = {
        "title": "Welcome to Maisha Uni Platform!",
        "body": "We are excited to launch our student success platform. This platform will help you discover opportunities, stay updated with announcements, and connect with institutions.",
        "pinned": True,
        "visible_until": "2024-12-31T23:59:59Z"
    }
    
    response = requests.post(f"{BASE_URL}/api/announcements/", json=announcement_data, headers=admin_headers)
    print_response("Create Announcement (Admin)", response)
    
    if response.status_code == 201:
        announcement = response.json()
        announcement_id = announcement['id']
        print(f"✓ Announcement created - ID: {announcement_id}")
        
        # Test getting specific announcement
        response = requests.get(f"{BASE_URL}/api/announcements/{announcement_id}/", headers=student_headers)
        print_response("Get Specific Announcement", response)
    
    # Try to create announcement as student (should fail)
    announcement_data2 = {
        "title": "Student Trying to Post",
        "body": "This should not work because students cannot post announcements.",
        "pinned": False
    }
    
    response = requests.post(f"{BASE_URL}/api/announcements/", json=announcement_data2, headers=student_headers)
    print_response("Create Announcement (Student - Should Fail)", response)
    
    if response.status_code == 403:
        print("✓ Correctly prevented student from creating announcement")
    
    # 5. Test Opportunities Endpoints
    print("\n5. TESTING OPPORTUNITIES ENDPOINTS")
    print("-" * 40)
    
    # Get opportunities
    response = requests.get(f"{BASE_URL}/api/opportunities/", headers=student_headers)
    print_response("Get Opportunities", response)
    
    if response.status_code == 200:
        opportunities = response.json()
        print(f"✓ Retrieved {len(opportunities)} opportunities")
    
    # Create opportunity as admin
    opportunity_data = {
        "title": "Software Engineering Internship",
        "description": "We are looking for passionate software engineering interns to join our team. You will work on real projects and learn from experienced mentors.",
        "category": "internship",
        "location": "Nairobi, Kenya (Hybrid)",
        "deadline": "2024-04-30",
        "requirements": {
            "skills": ["Python", "Django", "JavaScript", "Git"],
            "education": "Computer Science or related field",
            "year_of_study": "2nd Year or above",
            "duration": "3-6 months"
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/opportunities/", json=opportunity_data, headers=admin_headers)
    print_response("Create Opportunity (Admin)", response)
    
    if response.status_code == 201:
        opportunity = response.json()
        opportunity_id = opportunity['id']
        print(f"✓ Opportunity created - ID: {opportunity_id}")
        
        # Test getting specific opportunity
        response = requests.get(f"{BASE_URL}/api/opportunities/{opportunity_id}/", headers=student_headers)
        print_response("Get Specific Opportunity", response)
    
    # Create another opportunity for filtering test
    opportunity_data2 = {
        "title": "Data Science Scholarship 2024",
        "description": "Full scholarship for outstanding students pursuing Data Science and Machine Learning.",
        "category": "scholarship",
        "location": "Anywhere (Online)",
        "deadline": "2024-05-15",
        "requirements": {
            "gpa": "3.5 or above",
            "field": "STEM fields",
            "essay_required": True
        }
    }
    
    response = requests.post(f"{BASE_URL}/api/opportunities/", json=opportunity_data2, headers=admin_headers)
    if response.status_code == 201:
        print("✓ Second opportunity created for testing")
    
    # Test opportunity filters
    response = requests.get(f"{BASE_URL}/api/opportunities/?category=internship", headers=student_headers)
    print_response("Filter Opportunities by Category (internship)", response)
    
    # Try to create opportunity as student (should fail)
    opportunity_data3 = {
        "title": "Student Posted Opportunity",
        "description": "This should not work.",
        "category": "job",
        "location": "Nairobi",
        "deadline": "2024-12-31"
    }
    
    response = requests.post(f"{BASE_URL}/api/opportunities/", json=opportunity_data3, headers=student_headers)
    print_response("Create Opportunity (Student - Should Fail)", response)
    
    if response.status_code == 403:
        print("✓ Correctly prevented student from creating opportunity")
    
    # 6. Test Token Refresh
    print("\n6. TESTING TOKEN REFRESH")
    print("-" * 40)
    
    # Note: We need a refresh token for this, which we don't store in our current flow
    # This is just to show the endpoint exists
    print("Token refresh endpoint: /api/auth/refresh/")
    print("(Would need refresh token to test properly)")
    
    print("\n" + "="*50)
    print("TESTING COMPLETE")
    print("="*50)
    print("\nNext steps:")
    print("1. Check Swagger documentation: http://localhost:8000/swagger/")
    print("2. Test manually with the tokens above")
    print("3. Check Django admin: http://localhost:8000/admin/")

if __name__ == "__main__":
    # Check if requests is installed
    try:
        import requests
    except ImportError:
        print("Error: requests library not installed.")
        print("Install it with: pip install requests")
        sys.exit(1)
    
    # Check if server is likely running
    try:
        response = requests.get(BASE_URL, timeout=2)
    except requests.exceptions.ConnectionError:
        print(f"Error: Cannot connect to {BASE_URL}")
        print("Make sure the Django server is running with: python manage.py runserver")
        sys.exit(1)
    
    test_endpoints()