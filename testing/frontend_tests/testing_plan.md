# Exploratory Testing Plan

This document outlines exploratory tests to ensure the application meets the functional requirements and behaves as expected. Each test is designed to maximize coverage of the application's features.

---

## **1. User Profile Creation**
- Verify that a new user can successfully create a profile with valid inputs (username, email, password, etc.).
- Test profile creation with invalid inputs (e.g., missing fields, invalid email format, weak password).
- Check if duplicate email addresses are rejected during profile creation.
- Confirm that the system provides appropriate error messages for invalid inputs.
- Ensure that the profile creation process stores the correct data in the database.

---

## **2. User Login**
- Verify that a user can log in with valid credentials.
- Test login with invalid credentials (e.g., incorrect password, non-existent email).
- Check if the system locks the account after multiple failed login attempts.
- Confirm that the system provides appropriate error messages for invalid login attempts.
- Ensure that a valid session or token is created upon successful login.

---

## **3. Profile Access and Editing**
- Verify that a logged-in user can access their profile.
- Test editing profile fields (e.g., username, email, age, gender).
- Check if invalid inputs during profile editing are handled correctly.
- Confirm that changes to the profile are saved and reflected in the database.
- Ensure that unauthorized users cannot access or edit another user's profile.

---

## **4. Personal Biography**
- Verify that a user can write and update their personal biography.
- Test the character limit for the biography field.
- Check if special characters and emojis are supported in the biography.
- Confirm that the updated biography is displayed correctly on the user's profile.
- Ensure that unauthorized users cannot edit another user's biography.

---

## **5. Viewing Other User Profiles**
- Verify that a user can view the profiles of other users.
- Test if the profiles display the correct information (e.g., username, biography, age, etc.).
- Check if private information (e.g., email) is hidden from other users.
- Confirm that the system handles cases where a user tries to view a non-existent profile.

---

## **6. Sending "Likes"**
- Verify that a user can send a "like" to another user.
- Test if duplicate "likes" are prevented (e.g., liking the same user multiple times).
- Confirm that the recipient of the "like" is notified (if applicable).
- Ensure that the "like" is recorded in the database.
- Check if the system handles cases where a user tries to "like" a non-existent profile.

---

## **7. Viewing Matches**
- Verify that a user can view a list of users they have matched with.
- Test if the match list displays the correct information (e.g., usernames, profile pictures).
- Confirm that the match list updates in real-time when a new match is made.
- Ensure that the system handles cases where a user has no matches.

---

## **8. Personal Settings**
- Verify that a user can access and modify their personal settings (e.g., notifications, theme preferences, language).
- Test if changes to settings are saved and reflected in the database.
- Check if invalid inputs for settings are handled correctly.
- Confirm that the system provides appropriate feedback for successful or failed updates.

---

## **9. Terms of Service**
- Verify that a user can view the Terms of Service.
- Test if the Terms of Service page is accessible without logging in.
- Confirm that the Terms of Service content is displayed correctly.
- Ensure that the system handles cases where the Terms of Service page is unavailable.

---

## **10. Logout**
- Verify that a user can log out of the system.
- Test if the session or token is invalidated upon logout.
- Confirm that a logged-out user cannot access protected pages.
- Ensure that the system redirects the user to the login page after logout.

---

## **11. General Error Handling**
- Test how the system handles unexpected errors (e.g., database connection issues, server downtime).
- Verify that appropriate error messages are displayed to the user.
- Confirm that the system logs errors for debugging purposes.

---

## **12. Cross-Feature Testing**
- Test the flow of creating a profile, logging in, editing the profile, and logging out.
- Verify that a user can send a "like," view matches, and access settings in a single session.
- Check if changes to settings (e.g., language) are reflected across all features.

---

## **13. Security Testing**
- Verify that sensitive data (e.g., passwords, tokens) is encrypted and not exposed in the frontend.
- Test if unauthorized users can access protected endpoints.
- Check for vulnerabilities such as SQL injection, XSS, and CSRF.

---

## **14. Performance Testing**
- Test the response time for loading profiles, matches, and settings.
- Verify that the system can handle a large number of concurrent users.
- Check if the system gracefully handles slow network connections.

---

## **15. Mobile and Browser Compatibility**
- Verify that the application works correctly on different devices (e.g., mobile, tablet, desktop).
- Test the application on various browsers (e.g., Chrome, Firefox, Safari, Edge).
- Confirm that the UI is responsive and adapts to different screen sizes.