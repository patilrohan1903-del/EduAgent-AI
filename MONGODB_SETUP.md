# 🍃 MongoDB Atlas Setup Guide (Free)

Since Render is a cloud platform, it cannot connect to your "Local" database. You need a **Cloud Database**.
MongoDB Atlas provides a **Free Tier (512MB)** which is perfect for this project.

## Step 1: Create an Account
1.  Go to [mongodb.com/atlas/database](https://www.mongodb.com/atlas/database).
2.  Click **"Try Free"**.
3.  Sign up with Google or Email.

## Step 2: Create a Cluster
1.  After login, you will see a "Deploy a database" page.
2.  Select **"M0 Free"** (Shared).
3.  **Provider:** AWS (default is fine).
4.  **Region:** Choose usually the one closest to you (e.g., Singapore or N. Virginia).
5.  Click **"Create"**.

## Step 3: Setup User & IP Access
1.  **Username/Password:** Create a database user (e.g., `admin` and a strong password). **Save this password!**
2.  **IP Access:** Select **"Allow Access from Anywhere"** (0.0.0.0/0). This is crucial for Render to connect.

## Step 4: Get Connection String
1.  Go to **"Database"** (left menu) -> Click **"Connect"**.
2.  Select **"Drivers"** (Python).
3.  Copy the connection string. It will look like this:
    ```
    mongodb+srv://admin:<password>@cluster0.abcde.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
    ```

## Step 5: Update via Render Dashboard
1.  Replace `<password>` with the password you created in Step 3.
2.  Go to your **Render Dashboard** -> Select your Project.
3.  Click **"Environment"** -> **"Add Environment Variable"**.
4.  **Key:** `MONGO_URI`
5.  **Value:** (Paste your connection string here)

## Step 6: Redeploy
1.  Go to **"Events"** or **"Manual Deploy"** in Render.
2.  Click **"Clear build cache & deploy"** to be safe.

Your app should now connect successfully! 🚀
