# FitFlow Frontend - Developer Tips & Best Practices

## 🎯 Quick Reference

### Running Commands

```bash
# Development
npm run dev           # Start dev server on :3000

# Production
npm run build         # Build for production
npm start            # Start production server

# Code Quality
npm run lint         # Run ESLint

# Maintenance
npm install          # Install dependencies
npm update           # Update dependencies
npm audit            # Security audit
```

### Common File Locations

| What | Where |
|------|-------|
| API calls | `src/lib/apiClient.ts` |
| State stores | `src/lib/store.ts` |
| Components | `src/components/` |
| Pages | `src/app/[page]/page.tsx` |
| Global styles | `src/globals.css` |
| Config | Root directory (tailwind, next, tsconfig) |

---

## 💡 Development Tips

### 1. Using the API Client

```typescript
import apiClient from '@/lib/apiClient';

// GET
const data = await apiClient.get('/endpoint');

// POST with data
const response = await apiClient.post('/endpoint', {
  field: 'value'
});

// Error handling
try {
  const data = await apiClient.get('/endpoint');
} catch (error) {
  console.error('Error:', error.response?.data?.detail);
}
```

### 2. Using Zustand Stores

```typescript
import { useAuthStore, useWorkoutStore } from '@/lib/store';

export default function MyComponent() {
  // Get values
  const user = useAuthStore((state) => state.user);
  const workouts = useWorkoutStore((state) => state.workouts);

  // Update state
  const setWorkouts = useWorkoutStore((state) => state.setWorkouts);
  
  setWorkouts([...workouts, newWorkout]);
}
```

### 3. Protecting Routes

```typescript
'use client';

import { useRouter } from 'next/navigation';
import { useAuthStore } from '@/lib/store';
import { useEffect } from 'react';

export default function ProtectedPage() {
  const router = useRouter();
  const { isAuthenticated } = useAuthStore();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  // Protected content
  return <div>Protected Content</div>;
}
```

### 4. Creating New Pages

```bash
# 1. Create folder
mkdir -p src/app/feature-name

# 2. Create page.tsx
cat > src/app/feature-name/page.tsx << 'EOF'
'use client';

export default function FeaturePage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <h1>Feature Page</h1>
    </div>
  );
}
EOF
```

### 5. Adding Form Validation

```typescript
const [errors, setErrors] = useState<Record<string, string>>({});

const validateForm = (data: any) => {
  const newErrors: Record<string, string> = {};

  if (!data.email || !data.email.includes('@')) {
    newErrors.email = 'Valid email required';
  }

  if (!data.password || data.password.length < 8) {
    newErrors.password = 'Password must be 8+ characters';
  }

  setErrors(newErrors);
  return Object.keys(newErrors).length === 0;
};

const handleSubmit = (e: React.FormEvent) => {
  e.preventDefault();
  
  if (validateForm(formData)) {
    // Submit form
  }
};
```

---

## 🎨 Styling Guidelines

### Using Tailwind Classes

```tsx
// Button styles
<button className="btn-primary">Primary</button>
<button className="btn-secondary">Secondary</button>

// Card
<div className="card">Content</div>

// Form input
<input className="input-field" type="text" />

// Layout
<div className="grid grid-cols-1 md:grid-cols-2 gap-4">
  {/* Responsive grid */}
</div>
```

### Color Usage

```tsx
// Text colors
<p className="text-primary">Primary text</p>
<p className="text-secondary">Secondary text</p>

// Background colors
<div className="bg-blue-100">Light blue</div>
<div className="bg-red-500">Red background</div>

// Hover effects
<button className="hover:bg-gray-100">Hover me</button>

// Focus states
<input className="focus:ring-2 focus:ring-primary" />
```

### Responsive Classes

```tsx
// Mobile first
<div className="text-sm md:text-base lg:text-lg">
  Responsive text
</div>

// Hidden on mobile
<div className="hidden md:block">Desktop only</div>

// Show on mobile only
<div className="md:hidden">Mobile only</div>

// Responsive spacing
<div className="p-4 md:p-8 lg:p-12">Responsive padding</div>
```

---

## 🔒 Security Best Practices

### 1. Token Storage
```typescript
// Save token
localStorage.setItem('token', token);

// Retrieve token
const token = localStorage.getItem('token');

// Clear token on logout
localStorage.removeItem('token');
```

### 2. API Security
- Always use HTTPS in production
- Never expose API keys in client code
- Use environment variables for sensitive data
- CORS is configured on backend

### 3. Input Validation
- Validate all user inputs
- Sanitize data before sending to API
- Handle validation errors gracefully
- Show user-friendly error messages

### 4. Protected Routes
- Check authentication before rendering
- Redirect to login if not authenticated
- Store auth state in Zustand
- Use API client with automatic token handling

---

## 📊 Working with Charts

### Using Recharts

```typescript
import { LineChart, Line, XAxis, YAxis, ResponsiveContainer } from 'recharts';

const data = [
  { date: 'Jan 1', value: 100 },
  { date: 'Jan 2', value: 120 },
];

<ResponsiveContainer width="100%" height={300}>
  <LineChart data={data}>
    <XAxis dataKey="date" />
    <YAxis />
    <Line type="monotone" dataKey="value" stroke="#6366f1" />
  </LineChart>
</ResponsiveContainer>
```

### Chart Types Available
- LineChart - For trends (weight, calories over time)
- BarChart - For comparisons (workouts per day)
- PieChart - For distribution (workout types)
- AreaChart - For cumulative data

---

## 🐛 Debugging Tips

### 1. Check Network Requests
- Open DevTools (F12)
- Go to Network tab
- Look for API calls
- Check Response tab for API errors

### 2. Check State
```typescript
// Log store state
const state = useAuthStore.getState();
console.log('Auth state:', state);
```

### 3. Check Component Props
```typescript
console.log('Props:', props);
console.log('Component mounted');

return () => {
  console.log('Component unmounted');
};
```

### 4. Check for TypeScript Errors
```bash
# Find TypeScript errors
npm run build

# Check specific file
npx tsc --noEmit src/app/page.tsx
```

### 5. API Debugging
```typescript
// Log API requests
apiClient.interceptors.request.use(
  (config) => {
    console.log('Request:', config);
    return config;
  }
);

// Log API responses
apiClient.interceptors.response.use(
  (response) => {
    console.log('Response:', response);
    return response;
  }
);
```

---

## 🚀 Performance Optimization

### 1. Code Splitting
```typescript
import dynamic from 'next/dynamic';

// Load component only when needed
const HeavyComponent = dynamic(
  () => import('@/components/Heavy'),
  { loading: () => <div>Loading...</div> }
);
```

### 2. Memoization
```typescript
import { memo, useMemo } from 'react';

// Prevent unnecessary re-renders
const MemoComponent = memo(function Component({ data }) {
  const expensive = useMemo(() => {
    return data.map(/* ... */);
  }, [data]);

  return <div>{expensive}</div>;
});
```

### 3. Lazy Loading
```typescript
// Lazy load routes
const CoachPage = dynamic(
  () => import('@/app/coach/page'),
  { loading: () => <LoadingSpinner /> }
);
```

---

## 📱 Mobile Development

### Testing Responsive Design

```bash
# Dev Tools: F12 → Toggle device toolbar (Ctrl+Shift+M)
# Or resize browser window

# Mobile-first CSS
<div className="block md:grid md:grid-cols-2">
  Mobile blocks, desktop grid
</div>
```

### Touch-Friendly Design
```tsx
// Larger tap targets
<button className="px-4 py-3 min-h-[44px] min-w-[44px]">
  Touch-friendly
</button>

// Avoid hover-only interactions
<div className="group hover:bg-gray-100 active:bg-gray-200">
  Click/touch friendly
</div>
```

---

## 🧪 Testing Manual Cases

### Test User Flow
1. Register new user
2. Receive token
3. Access dashboard
4. Create workout
5. Log meal
6. Chat with coach
7. View progress
8. Logout

### Test Error Cases
1. Invalid login credentials
2. Network timeout
3. API errors (500, 404)
4. Missing required fields
5. Session expiration

### Test Edge Cases
1. Rapid clicking
2. Navigation during load
3. Offline mode
4. Very long text inputs
5. Special characters in inputs

---

## 📚 Learning Resources

### Official Documentation
- [Next.js Docs](https://nextjs.org/docs)
- [React Docs](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Zustand](https://github.com/pmndrs/zustand)
- [Axios](https://axios-http.com)

### Video Tutorials
- Next.js App Router by Vercel
- TypeScript for React Developers
- Tailwind CSS Tutorial
- React Hooks Deep Dive

### Community
- Stack Overflow (tag: next.js, react, typescript)
- GitHub Discussions
- Discord communities
- Reddit: r/reactjs, r/typescript

---

## 🎓 Code Examples

### Complete API Integration Example

```typescript
'use client';

import { useEffect, useState } from 'react';
import apiClient from '@/lib/apiClient';

export default function Example() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      try {
        const response = await apiClient.get('/endpoint');
        setData(response.data);
      } catch (err: any) {
        setError(err.response?.data?.detail || 'Error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div>Loading...</div>;
  if (error) return <div className="text-red-600">{error}</div>;

  return <div>{JSON.stringify(data)}</div>;
}
```

### Complete Form Example

```typescript
'use client';

import { useState } from 'react';
import apiClient from '@/lib/apiClient';

export default function FormExample() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const response = await apiClient.post('/endpoint', formData);
      console.log('Success:', response.data);
      // Reset form
      setFormData({ name: '', email: '' });
    } catch (err: any) {
      setErrors({
        submit: err.response?.data?.detail || 'Submission failed'
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleChange}
          className="input-field"
          placeholder="Name"
        />
        {errors.name && <p className="text-red-600">{errors.name}</p>}
      </div>

      <button type="submit" disabled={loading} className="btn-primary">
        {loading ? 'Submitting...' : 'Submit'}
      </button>

      {errors.submit && (
        <p className="text-red-600">{errors.submit}</p>
      )}
    </form>
  );
}
```

---

## ✅ Pre-Deployment Checklist

- [ ] All pages working correctly
- [ ] No console errors
- [ ] API integration tested
- [ ] Mobile responsive
- [ ] All links working
- [ ] Forms validating properly
- [ ] Error handling in place
- [ ] Environment variables set
- [ ] Build completes successfully: `npm run build`
- [ ] No TypeScript errors
- [ ] Performance acceptable
- [ ] Security best practices followed

---

**Happy coding! 🚀**

For more detailed information, see the other documentation files:
- `SETUP.md` - Installation guide
- `FEATURES.md` - Feature documentation
- `API.md` - API reference
- `README.md` - Project overview
