# Jammin
Jammin is a project created for SENG 401 - Software Architecture that uses ChatGPT to parse a user’s Spotify analytics and match them with people with similar music taste. Matches are made based on both user’s top artists, songs and genres, combining to generate a compatibility score between both parties.

## Features
### Matching
You can scroll through people's profile, seeing their compatibility score with you, description of why they received that match score and more Spotify data of your matched user. Data visible includes top songs, top artists and top genres for each user. 
![Screenshot of Matching Page from Jammin'](/readme_images/jammin_matching.jpg)
![Screenshot of Matching Page with top songs from Jammin'](/readme_images/jammin_matching_top_songs.jpg)
![Screenshot of Matching Page with description from Jammin'](/readme_images/jammin_matching_desc.jpg)

### Profile
You can see your own Spotify data and personal Jammin' data on the Profile page. On the public profile tab, you can see your Spotify name, top songs and top artists, as well as additional prompts to add to your public profile. On the Jammin' profile tab, you see the data associated with your Jammin' profile. This includes name, email, password, along with personal profile data like age, gender, bio, school, occupation, and what you are looking for on Jammin'.
![Screenshot of Profile Page from Jammin'](/readme_images/jammin_profile.jpg)

### Matches
After matching with users, you can see who you matched with on the Matches page. If both of you matched with each other, you can see that persons profile name, match score and date you matched on. If you drop down that menu, you can see the Jammin' data associated with that user. This allows you to see the more personal data of the people you matched with, and get to know that person better.

### Log Out
If you wanted to remove your spotify account or add a new user to Jammin' you can use the logout button to remove your Spotify account and logout your Jammin' profile. This allows you to sign in or sign up with a different account, making Jammin' usable on one device. 

## Tech Stack
- **Frontend**: Vercel, React + Vite
- **Backend**: Flask
- **Database**: MySQL (Local), PostgreSQL (Hosted), Supabase
- **Testing**: Mockito

## How to Use
### Hosted:
To use Jammin' online, you simply visit [Jammin'](https://jammin-app.vercel.app) and create an account. In the login/signup process, you must link your Spotify account and authorize Spotify access for Jammin'. From there, you can simply browse Jammin', where you can create matches and update our account throughout the app!

### Local:
The local version of Jammin is set up on a separate branch from main in this repo, and is created via Docker's containerization. After cloning ___, you must open Docker Desktop and run `docker compose up --build` in the jammin-app folder to create the project. This will establish the frontend (Port 5173), backend (Port 5001) and SQL containers for local use. Then, you must create a connection with MySQL to port 3307 where the SQL database is hosted. This should create a connection between Jammin' and your local database, and allow you to use the app like above.

## Future Plans
Jammin' allows for expansion in various ways, some of which we already have planned out. Messaging was a big plan for our development cycle, where we wanted matched users to be able to message each other over Jammin' and actually talk about their music interests. We also wanted to add additional data to the account, such as prompts to display on the users profile to customize your account more. We were also looking into adding photos to your public profile, further personalizing the data users see when matching together.

## Credits: 
Samiul Haque,
Keeryn Johnson,
Elias Poitras-Whitecalf,
Petr Dubovsky,
Ryan Graham,
Evan Mann
