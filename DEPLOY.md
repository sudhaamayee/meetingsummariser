# 🚀 Deployment Guide - Meeting Summarizer

## ✅ What You Need
- GitHub repository (you have: `sudhaamayee/meetingsummariser`)
- Vercel account (free)
- Render account (free)

---

## 📋 Step-by-Step Deployment

### **STEP 1: Fix Vercel Deployment (Frontend)**

Your Vercel deployment failed because of configuration. Here's how to fix it:

#### **Option A: Redeploy with Correct Settings**

1. **Go to your Vercel project:** https://vercel.com/sudhaamayees-projects/meetingsummariser
2. **Click:** "Settings" (top menu)
3. **Scroll to:** "Build & Development Settings"
4. **Update these settings:**
   ```
   Framework Preset: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   Install Command: npm install
   ```
5. **Click:** "Save"
6. **Go to:** "Deployments" tab
7. **Click:** "Redeploy" on the latest deployment

#### **Option B: Use vercel.json (Already Created)**

I just created `vercel.json` in your root directory. Now:

1. **Commit and push:**
   ```bash
   git add vercel.json
   git commit -m "Add Vercel configuration"
   git push
   ```

2. **Vercel will auto-deploy** with correct settings

---

### **STEP 2: Deploy Backend to Render**

1. **Go to:** https://dashboard.render.com
2. **Click:** "New +" → "Web Service"
3. **Connect repository:** `sudhaamayee/meetingsummariser`
4. **Fill in these details:**

   **Name:** `meeting-summarizer-api`
   
   **Region:** Choose closest to you
   
   **Branch:** `master`
   
   **Root Directory:** `backend`
   
   **Runtime:** `Python 3`
   
   **Build Command:**
   ```bash
   pip install -r requirements.txt
   ```
   
   **Start Command:**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

5. **Instance Type:** Free

6. **Advanced → Environment Variables:**
   
   Click "Add Environment Variable" for each:
   ```
   USE_STUB=1
   HUGGINGFACE_DEVICE=cpu
   UPLOAD_DIR=/tmp/uploads
   MONGODB_URI=mongodb://localhost:27017
   MONGODB_DB=meeting_ai
   ```

7. **Click:** "Create Web Service"

8. **Wait ~5 minutes** for deployment

9. **Copy your backend URL** (e.g., `https://meeting-summarizer-api.onrender.com`)

---

### **STEP 3: Update Frontend Environment Variable**

1. **Go back to Vercel:** https://vercel.com/sudhaamayees-projects/meetingsummariser
2. **Click:** "Settings" → "Environment Variables"
3. **Add new variable:**
   ```
   Name: VITE_API_BASE
   Value: https://meeting-summarizer-api.onrender.com
   ```
   (Use your actual Render URL from Step 2)

4. **Click:** "Save"
5. **Go to:** "Deployments" → "Redeploy"

---

### **STEP 4: Test Your Deployed App**

1. **Open your Vercel URL:** `https://meetingsummariser-git-master-sudhaamayees-projects.vercel.app`
2. **Upload a test file**
3. **Should work!** 🎉

---

## 🔧 Troubleshooting

### **Vercel Build Failed**

**Error:** `Command "npm run build" exited with 126`

**Fix:**
1. Make sure `vercel.json` is in root directory
2. Set Root Directory to `frontend` in Vercel settings
3. Redeploy

---

### **Backend Not Responding**

**Issue:** Frontend can't connect to backend

**Fix:**
1. Check Render logs for errors
2. Verify backend URL in Vercel environment variables
3. Make sure backend is not sleeping (free tier sleeps after 15 min)

---

### **CORS Errors**

**Issue:** Browser blocks API requests

**Fix:** Update `backend/app/main.py` CORS settings:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://meetingsummariser-git-master-sudhaamayees-projects.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📊 Your Deployed URLs

**Frontend (Vercel):**
- Production: `https://meetingsummariser-git-master-sudhaamayees-projects.vercel.app`
- Custom domain: (optional, configure in Vercel)

**Backend (Render):**
- API: `https://meeting-summarizer-api.onrender.com`
- Docs: `https://meeting-summarizer-api.onrender.com/docs`

---

## ⚠️ Important Notes

### **Free Tier Limitations:**

**Vercel:**
- ✅ Always on
- ✅ Unlimited bandwidth
- ✅ Automatic HTTPS
- ✅ Free custom domain

**Render:**
- ⚠️ Sleeps after 15 min inactivity
- ⚠️ First request takes ~30 seconds to wake
- ⚠️ 750 hours/month free
- ⚠️ Ephemeral storage (files deleted on restart)

### **Production Recommendations:**

1. **Upgrade Render to paid tier** ($7/month) for always-on backend
2. **Use cloud storage** (AWS S3, Cloudinary) for uploaded files
3. **Add authentication** to prevent abuse
4. **Set up MongoDB Atlas** for persistent data storage
5. **Add rate limiting** to API endpoints

---

## 🎯 Quick Commands

**Commit and push changes:**
```bash
git add .
git commit -m "Update deployment config"
git push
```

**Check Vercel deployment:**
```bash
# Vercel auto-deploys on push
# Check: https://vercel.com/sudhaamayees-projects/meetingsummariser
```

**Check Render deployment:**
```bash
# Render auto-deploys on push
# Check: https://dashboard.render.com
```

---

## 🎉 Success Checklist

- [ ] `vercel.json` created in root
- [ ] Vercel settings updated (Root Directory: `frontend`)
- [ ] Backend deployed to Render
- [ ] Environment variables set on both platforms
- [ ] Frontend can connect to backend
- [ ] Upload and transcription working
- [ ] App is live and accessible!

---

## 📚 Resources

- **Vercel Docs:** https://vercel.com/docs
- **Render Docs:** https://render.com/docs
- **Your GitHub Repo:** https://github.com/sudhaamayee/meetingsummariser

---

**Need help?** Check the logs:
- **Vercel:** Deployments → Click on deployment → View logs
- **Render:** Dashboard → Your service → Logs tab
