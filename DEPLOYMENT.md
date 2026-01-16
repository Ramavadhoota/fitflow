# FitFlow Frontend - Deployment Guide

## Overview
FitFlow is a modern Next.js frontend for an AI-powered fitness platform. This guide covers deployment options.

## Deployment Options

### 1. Vercel (Recommended - Free & Easy)

**Best for:** Production-ready deployments with automatic updates

**Steps:**
1. Push your code to GitHub
2. Go to [vercel.com](https://vercel.com)
3. Click "New Project"
4. Import your GitHub repository
5. Set environment variables:
   - `NEXT_PUBLIC_API_URL`: Your backend API URL
6. Click "Deploy"

**Auto-Deploy:** Every push to main branch automatically deploys

### 2. Docker + Railway

**Steps:**
```bash
# Build Docker image
docker build -t fitflow-frontend .

# Test locally
docker run -p 3000:3000 fitflow-frontend

# Deploy to Railway
railway link
railway up
```

### 3. Docker + Render

**Steps:**
1. Push to GitHub
2. Go to [render.com](https://render.com)
3. Create new Web Service
4. Select your GitHub repository
5. Set:
   - Build Command: `npm run build`
   - Start Command: `npm start`
   - Environment: Node 18
6. Add environment variables
7. Deploy

### 4. Netlify

**Steps:**
1. Connect GitHub repository
2. Build settings:
   - Build command: `npm run build`
   - Publish directory: `.next`
3. Add environment variables
4. Deploy

## Environment Variables

### Production
```env
NEXT_PUBLIC_API_URL=https://your-api-domain.com
```

### Development
```env
NEXT_PUBLIC_API_URL=http://localhost:8001
```

## Performance Tips

- Images are optimized automatically
- Static pages are pre-rendered
- Dynamic pages use ISR (Incremental Static Regeneration)
- Tailwind CSS is minified

## Monitoring

Set up monitoring for:
- Page load times
- API response times
- Error tracking (Sentry recommended)
- User analytics (Google Analytics)

## Scaling

As traffic grows:
1. Use CDN (Vercel/Netlify include this)
2. Enable caching headers
3. Monitor backend API capacity
4. Consider API rate limiting

## Troubleshooting

### 404 Errors
- Ensure all pages are created in `/src/app`
- Check that page.tsx files export default components

### API Connection Issues
- Verify `NEXT_PUBLIC_API_URL` is correct
- Check backend is running
- Check CORS headers on backend

### Build Failures
- Run `npm install` to ensure dependencies
- Check Node.js version (18+)
- Check for TypeScript errors: `npm run type-check`

## Cost Estimate (Monthly)

| Service | Free Tier | Premium |
|---------|-----------|---------|
| Vercel | Free | $20+/month |
| Railway | $5 trial | Pay-as-you-go |
| Render | Limited | $7+/month |
| Netlify | Free | $19+/month |

## Next Steps

1. **Set up monitoring:** Add error tracking and analytics
2. **Optimize images:** Compress and optimize media files
3. **Add PWA:** Make it installable as an app
4. **Mobile testing:** Test on various devices
5. **Performance:** Run Lighthouse audits regularly

## Support

For deployment issues:
- Check service provider documentation
- Review backend API logs
- Check browser console for errors
- Monitor server uptime
