# 🏛️ Yappy's Pattern Library

**Created**: March 16, 2026  
**Source**: Wedding Wall Project (Phases 1-6)  
**Purpose**: Reusable patterns for future projects

---

## 📋 Pattern Index

1. [CORS & File Upload Patterns](#cors--file-upload-patterns)
2. [Auth & Join Flow Patterns](#auth--join-flow-patterns)
3. [Real-time Data Patterns](#real-time-data-patterns)
4. [AWS S3 Integration Patterns](#aws-s3-integration-patterns)
5. [Database & ORM Patterns](#database--orm-patterns)
6. [UI/UX Patterns](#uiux-patterns)

---

## 🔴 CORS & File Upload Patterns

### Pattern: Backend File Upload (NOT Pre-signed URLs)

**Problem**: Browser can't upload directly to S3 (CORS blocks it)

**Solution**: Create backend endpoint that handles upload

```typescript
// Route: POST /api/upload
export async function POST(request: NextRequest) {
  const formData = await request.formData();
  const file = formData.get('file') as File;
  const bucket = process.env.AWS_S3_BUCKET!;
  
  // Convert to buffer
  const buffer = Buffer.from(await file.arrayBuffer());
  
  // Upload server-side (no CORS issues)
  const s3Key = `uploads/${Date.now()}-${file.name}`;
  const result = await uploadToS3(s3Key, buffer, file.type);
  
  return NextResponse.json(result);
}
```

**Pros:**
- ✅ No CORS configuration needed
- ✅ Credentials never exposed to client
- ✅ Can validate, process, or transform files
- ✅ Full server-side control

**Cons:**
- ❌ More server load
- ❌ File size limited by server memory
- ❌ Slower for large files

**When to Use:**
- ✅ Need server-side validation
- ✅ Security is paramount
- ✅ File sizes < 100MB
- ✅ Want to add processing (resize, compress, etc)

**When NOT to Use:**
- ❌ Huge files (> 500MB) - use pre-signed URLs instead
- ❌ Ultra-high upload volume
- ❌ Server resources limited

---

### Pattern: Image Proxy (NOT Direct S3 URLs)

**Problem**: Browser requests to S3 are blocked by CORS/OpaqueResponseBlocking

**Solution**: Create proxy endpoint that fetches from S3 server-side

```typescript
// Route: GET /api/image?key=photos/...
export async function GET(request: NextRequest) {
  const s3Key = request.nextUrl.searchParams.get('key');
  
  // Security: Whitelist allowed prefixes
  if (!s3Key?.startsWith('photos/')) {
    return NextResponse.json({ error: 'Invalid' }, { status: 403 });
  }
  
  // Fetch from S3 server-side
  const s3Client = new S3Client({ region, credentials });
  const response = await s3Client.send(
    new GetObjectCommand({ Bucket, Key: s3Key })
  );
  
  const buffer = await response.Body!.transformToByteArray();
  
  return new NextResponse(Buffer.from(buffer), {
    headers: {
      'Content-Type': response.ContentType || 'image/jpeg',
      'Cache-Control': 'public, max-age=31536000' // S3 keys immutable
    }
  });
}
```

**Gallery Usage:**
```tsx
// Before (blocked by CORS):
<img src="https://bucket.s3.amazonaws.com/photos/..." />

// After (via proxy):
<img src={`/api/image?key=${encodeURIComponent(s3Key)}`} />
```

**Pros:**
- ✅ No CORS configuration
- ✅ Aggressive caching possible
- ✅ Can add watermarking, resizing
- ✅ Can track image access

**Cons:**
- ❌ Extra server request per image
- ❌ Network bottleneck if many images

**When to Use:**
- ✅ Want to avoid S3 CORS config
- ✅ Need tight access control
- ✅ Want to add image processing
- ✅ Images < 10MB typical

---

## 🟢 Auth & Join Flow Patterns

### Pattern: URL Code Auto-Join (Seamless UX)

**Problem**: Guest gets invite link with code, but page shows form instead of immediately joining

**Solution**: Detect code in URL, auto-validate, auto-redirect

```typescript
// app/auth/join/page.tsx
function JoinContent() {
  const router = useRouter();
  const searchParams = useSearchParams();

  useEffect(() => {
    const code = searchParams.get('code');
    if (code) {
      // Auto-join silently
      fetch(`/api/session?code=${code}`)
        .then(r => r.json())
        .then(session => router.push(`/gallery?sessionId=${session.id}`))
        .catch(() => router.push('/')); // Fallback
    }
  }, [searchParams]);

  // Show loading screen while validating
  return <LoadingSpinner />;
}

export default function JoinPage() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <JoinContent />
    </Suspense>
  );
}
```

**UX Flow:**
```
Guest clicks link with ?code=ABC123
↓
Page shows loading spinner
↓
Backend validates code silently
↓
Auto-redirect to main content
↓
No form shown (seamless!)
```

**Key Points:**
- ✅ Wrap with Suspense for useSearchParams
- ✅ Graceful fallback if code invalid
- ✅ No user interaction needed
- ✅ Smooth loading experience

**When to Use:**
- ✅ Invite links with codes
- ✅ Magic links
- ✅ OAuth callback flows

---

### Pattern: Guest Creation On-Demand

**Problem**: Can't create upload token without guestId, but guest doesn't exist yet

**Solution**: Create guest during first upload

```typescript
// In POST /api/upload handler
let guest = await prisma.guest.findFirst({
  where: { sessionId, name: guestName }
});

if (!guest) {
  guest = await prisma.guest.create({
    data: { sessionId, name: guestName }
  });
}

// Now use guest.id for upload
```

**Benefits:**
- ✅ No pre-registration needed
- ✅ Lower friction for guests
- ✅ Avoid foreign key constraint violations
- ✅ Guests identified by name

**When to Use:**
- ✅ Passwordless/anonymous systems
- ✅ One-time event apps
- ✅ Guest submission flows

---

## 🔵 Real-time Data Patterns

### Pattern: Polling for New Data

**Problem**: Gallery needs to show new photos in real-time without WebSocket

**Solution**: Poll server every N seconds

```typescript
useEffect(() => {
  const fetchPhotos = async () => {
    const response = await fetch(`/api/photos?sessionId=${sessionId}`);
    const data = await response.json();
    setPhotos(data);
  };

  // Fetch immediately
  fetchPhotos();

  // Then poll every 3 seconds
  const interval = setInterval(fetchPhotos, 3000);
  
  return () => clearInterval(interval);
}, [sessionId]);
```

**Pros:**
- ✅ Simple to implement
- ✅ Works everywhere (no WebSocket complexity)
- ✅ Good for < 100 concurrent users

**Cons:**
- ❌ Network overhead
- ❌ Slight delay (up to 3 sec)
- ❌ Not scalable for 1000+ users

**When to Use:**
- ✅ Small event apps (< 100 guests)
- ✅ Acceptable 3-5 sec delays
- ✅ Want to avoid WebSocket infrastructure

**When NOT to Use:**
- ❌ Thousands of concurrent users
- ❌ Need instant updates
- ❌ High traffic app

---

## 🟠 AWS S3 Integration Patterns

### Pattern: Secure S3 Credentials in Next.js

**Setup in `.env.local`:**
```
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=ap-southeast-1
AWS_S3_BUCKET=my-bucket
```

**Server-side Usage (safe):**
```typescript
// lib/s3.ts
import { S3Client } from "@aws-sdk/client-s3";

const s3Client = new S3Client({
  region: process.env.AWS_REGION,
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID!,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY!,
  },
});

export default s3Client;
```

**Key Rules:**
- ✅ Use IAM user credentials (not root)
- ✅ Only server-side (never expose to client)
- ✅ Rotate keys regularly
- ✅ S3 bucket should be **private** (no public access)
- ✅ Use API proxy for client access

**Anti-patterns:**
- ❌ Never use root AWS credentials
- ❌ Never expose credentials in code
- ❌ Never commit `.env.local` to git
- ❌ Never make S3 bucket public

---

### Pattern: S3 Key Generation

**Safe Pattern**: Include context and timestamp

```typescript
// Good: Date.now() ensures uniqueness
const s3Key = `photos/${sessionId}/${Date.now()}-${sanitizedFileName}`;

// Bad: Just the filename (conflicts possible)
const s3Key = `photos/${fileName}`;

// Bad: UUID without timestamp (harder to debug)
const s3Key = `photos/${uuidv4()}`;
```

**For Organization:**
```
s3Key = `{category}/{context}/{timestamp}-{identifier}-{filename}`

Example:
photos/session-123/1710657600000-guest-john-wedding.jpg
       ^^^^^^^^^^^  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
       context     timestamp ensures uniqueness + readable
```

**Benefits:**
- ✅ Filesystem-like organization
- ✅ Timestamp prevents collisions
- ✅ Easy to debug (human readable)
- ✅ Easy to delete by prefix

---

## 🟣 Database & ORM Patterns

### Pattern: Session with Expiry

**Schema:**
```prisma
model WeddingSession {
  id        String   @id @default(cuid())
  code      String   @unique
  expiresAt DateTime
  createdAt DateTime @default(now())
  
  guests    Guest[]
  photos    Photo[]
}
```

**Validation:**
```typescript
const session = await prisma.weddingSession.findUnique({
  where: { id: sessionId }
});

if (!session || new Date() > session.expiresAt) {
  return NextResponse.json(
    { error: 'Session expired' },
    { status: 410 }
  );
}
```

**Key Points:**
- ✅ Use DateTime for expiry
- ✅ Check on every request
- ✅ 410 Gone status code for expired
- ✅ Consider cleanup job for old sessions

---

### Pattern: One-to-Many with Validation

**Problem**: Create photo record linked to session & guest

**Solution:**
```prisma
model Photo {
  id        String @id @default(cuid())
  sessionId String // Must exist in WeddingSession
  guestId   String // Must exist in Guest
  s3Key     String
  s3Url     String
  
  session   WeddingSession @relation(fields: [sessionId], references: [id])
  guest     Guest @relation(fields: [guestId], references: [id])
}
```

**Safe Creation:**
```typescript
// Validate both before creating
const session = await prisma.weddingSession.findUnique({
  where: { id: sessionId }
});
const guest = await prisma.guest.findUnique({
  where: { id: guestId }
});

if (!session || !guest) {
  throw new Error('Invalid session or guest');
}

const photo = await prisma.photo.create({
  data: {
    sessionId,
    guestId,
    s3Key,
    s3Url
  }
});
```

---

## 🟡 UI/UX Patterns

### Pattern: Dark Mode Implementation (Tailwind v4)

**Problem**: Implementing class-based dark mode in Tailwind v4 where `darkMode: 'class'` configuration is deprecated/changed.

**Solution**: Use CSS variables and `@custom-variant` in global CSS.

1. **Global CSS Configuration (`app/globals.css`)**:
```css
@import "tailwindcss";

/* 1. Define custom variant for class-based toggling */
@custom-variant dark (&:where(.dark, .dark *));

/* 2. Define theme variables */
:root {
  --background: #ffffff;
  --foreground: #171717;
}

/* 3. Override variables for dark mode */
.dark {
  --background: #0a0a0a;
  --foreground: #ededed;
}

/* 4. Apply variables to body */
body {
  background: var(--background);
  color: var(--foreground);
}
```

2. **React Component Logic (`components/Navbar.tsx`)**:
```tsx
export default function Navbar() {
  const [isDarkMode, setIsDarkMode] = useState(false); // Default: Light
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    // OPTION A: Default to Light Mode (Recommended)
    // No action needed, state starts as false.

    // OPTION B: Default to System Preference
    /*
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      setIsDarkMode(true);
      document.documentElement.classList.add('dark');
    }
    */
  }, []);

  const toggleDarkMode = () => {
    if (isDarkMode) {
      document.documentElement.classList.remove('dark');
      setIsDarkMode(false);
    } else {
      document.documentElement.classList.add('dark');
      setIsDarkMode(true);
    }
  };

  if (!mounted) return null; // Avoid hydration mismatch

  return (
    <button onClick={toggleDarkMode}>
      {isDarkMode ? '☀️' : '🌙'}
    </button>
  );
}
```

3. **Usage in Components**:
```tsx
<div className="bg-white dark:bg-black text-gray-900 dark:text-white">
  <h1 className="text-blue-600 dark:text-blue-400">Hello World</h1>
  <div className="bg-gray-100 dark:bg-gray-800 p-4 rounded">
    Card Content
  </div>
</div>
```

**Key Points:**
- ✅ **Tailwind v4 Specific**: Uses `@custom-variant` instead of `tailwind.config.js`.
- ✅ **Class-Based**: controlled by `.dark` class on `<html>` tag.
- ✅ **Hydration Safe**: `mounted` check prevents server/client mismatch.
- ✅ **Granular Control**: Use `dark:` prefix for specific overrides.
- ✅ **CSS Variables**: Theme updates automatically with variables.

---

### Pattern: Handling Global CSS Conflicts (Tailwind)

**Problem**: Utility classes (e.g., `text-gray-900`) being ignored in specific contexts due to high-specificity global styles.

**Scenario**: 
A global rule like `p { color: var(--foreground); }` in `globals.css` can override Tailwind utility classes because element-level selectors in CSS often have unexpected specificity or cascading behavior when mixed with utility classes.

**Solution**: 
Avoid enforcing colors on global tags if you plan to use utility classes.

**Incorrect (`app/globals.css`)**:
```css
p {
  color: var(--foreground); /* ❌ Overrides utility classes */
}
```

**Correct (`app/globals.css`)**:
```css
p {
  /* ✅ Let utility classes handle color */
}
```

**Why**: 
Tailwind works best when the "base" styles are minimal and unopinionated. Forcing a color globally means you have to use `!important` or high-specificity overrides later, which breaks the utility-first workflow.

---


### Pattern: Robust Clipboard Copy (PWA/Mobile Support)

**Problem**: 
`navigator.clipboard.writeText()` fails in non-secure contexts (like local IP addresses for mobile testing) or older WebViews, throwing `undefined is not an object (evaluating 'navigator.clipboard.writeText')`.

**Solution**: 
Use a fallback strategy combining modern Clipboard API with legacy `document.execCommand('copy')`.

**Implementation**:
```typescript
const copyToClipboard = (text: string) => {
  if (navigator.clipboard && window.isSecureContext) {
    // Modern & Secure
    navigator.clipboard.writeText(text);
  } else {
    // Fallback: Invisible Textarea
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.position = "fixed";
    textArea.style.left = "-9999px";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    try {
      document.execCommand('copy');
    } catch (err) {
      console.error('Fallback failed', err);
    }
    document.body.removeChild(textArea);
  }
};
```

---

### Pattern: Form with Loading State

**State Management:**
```typescript
const [loading, setLoading] = useState(false);
const [error, setError] = useState('');
const [success, setSuccess] = useState(false);

const handleSubmit = async (e) => {
  e.preventDefault();
  setLoading(true);
  setError('');
  
  try {
    const response = await fetch('/api/endpoint', {
      method: 'POST',
      body: JSON.stringify(data)
    });
    
    if (!response.ok) throw new Error('Failed');
    
    setSuccess(true);
    // Redirect or reset form
  } catch (err) {
    setError(err.message);
  } finally {
    setLoading(false);
  }
};
```

**Button State:**
```tsx
<button disabled={!formValid || loading}>
  {loading ? 'Uploading...' : 'Submit'}
</button>
```

---

### Pattern: Real-time Polling Indicator

**Show users data is updating:**
```tsx
const [isPolling, setIsPolling] = useState(true);

useEffect(() => {
  const interval = setInterval(async () => {
    setIsPolling(true);
    await fetchPhotos();
    setIsPolling(false);
  }, 3000);
  
  return () => clearInterval(interval);
}, []);

return (
  <div>
    {isPolling && <Spinner />}
    {/* Photos */}
  </div>
);
```

---

### Pattern: Masonry Gallery Layout

```tsx
<div
  className="columns-1 sm:columns-2 lg:columns-3 gap-4 space-y-4"
  style={{ columnFill: 'auto' }}
>
  {items.map(item => (
    <div key={item.id} className="break-inside-avoid">
      <img src={item.image} />
    </div>
  ))}
</div>
```

**Key Classes:**
- `columns-1/2/3` - Number of columns
- `gap-4` - Space between items
- `space-y-4` - Vertical spacing
- `break-inside-avoid` - Keep item together
- `column-fill: auto` - Fill left-to-right

---

### Pattern: Glassmorphic Responsive Navbar

**Problem**: Need a modern, sticky navigation bar that works on mobile and desktop with a "glass" effect.

**Solution**: Tailwind utilities for backdrop blur and state for mobile menu.

```tsx
// components/Navbar.tsx
export default function Navbar() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  // 1. Handle scroll for shrinking effect
  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav className={`fixed top-0 z-50 w-full transition-all ${scrolled ? 'py-2' : 'py-4'}`}>
      <div className="max-w-7xl mx-auto px-4">
        {/* 2. Glassmorphism Container */}
        <div className={`
          backdrop-blur-xl border border-white/40 dark:border-white/10 
          rounded-3xl px-6 py-3 shadow-lg transition-all
          ${scrolled ? 'bg-white/90 dark:bg-black/80' : 'bg-white/60 dark:bg-black/40'}
        `}>
          <div className="flex justify-between items-center">
            {/* Logo */}
            <Link href="/" className="font-bold text-xl">Brand</Link>

            {/* Desktop Nav */}
            <div className="hidden md:flex space-x-1">
              {navItems.map(item => (
                <Link 
                  key={item.name} 
                  href={item.href}
                  className="px-4 py-2 rounded-full hover:bg-orange-50 dark:hover:bg-white/10 transition-colors"
                >
                  {item.name}
                </Link>
              ))}
            </div>

            {/* Mobile Toggle */}
            <button 
              className="md:hidden p-2"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              <Icon icon={mobileMenuOpen ? faTimes : faBars} />
            </button>
          </div>

          {/* 3. Mobile Menu Dropdown (Smooth Transition) */}
          <div 
            className={`md:hidden overflow-hidden transition-all duration-300 ease-in-out ${
              mobileMenuOpen 
                ? 'max-h-96 opacity-100 mt-2 border-t border-gray-100 dark:border-white/10 pt-1' 
                : 'max-h-0 opacity-0 mt-0 pt-0 border-transparent'
            }`}
          >
            <div className="space-y-1">
              {navItems.map(item => (
                <Link 
                  key={item.name}
                  href={item.href}
                  className="block px-4 py-3 rounded-xl hover:bg-orange-50 dark:hover:bg-white/10 transition-all duration-300"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  {item.name}
                </Link>
              ))}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
```

**Key Features:**
- ✅ **Glass Effect**: `backdrop-blur-xl` + semi-transparent `bg-white/60`.
- ✅ **Scroll Awareness**: Shrinks padding and increases opacity on scroll.
- ✅ **Smooth Mobile Transition**: Uses `max-height` and `opacity` to animate the menu open/closed instead of sudden DOM removal.
- ✅ **Floating Pill Design**: Uses `rounded-3xl` and `margin` instead of full-width.
- ✅ **Mobile Responsive**: Hides desktop menu, shows hamburger on mobile.

---

### Pattern: Floating Action Button (FAB)

**Problem**: Need a prominent primary action accessible from anywhere on the page (e.g., "Upload", "Compose", "Chat").

**Solution**: Fixed position button with high z-index and elevation.

```tsx
// components/Fab.tsx
export default function FloatingActionButton({ href, icon, label }: FabProps) {
  return (
    <div className="fixed bottom-6 right-6 z-50">
      <Link href={href}>
        <button className="
          group flex items-center justify-center
          bg-gradient-to-r from-orange-500 to-pink-500
          text-white shadow-lg hover:shadow-xl hover:scale-105
          transition-all duration-300
          h-14 w-14 rounded-full
          md:w-auto md:px-6 md:rounded-full
        ">
          <FontAwesomeIcon icon={icon} className="text-xl" />
          <span className="hidden md:inline-block ml-2 font-semibold whitespace-nowrap overflow-hidden max-w-0 group-hover:max-w-xs transition-all duration-500">
            {label}
          </span>
        </button>
      </Link>
    </div>
  );
}
```

**Key Features:**
- ✅ **Fixed Position**: `fixed bottom-6 right-6 z-50` ensures visibility.
- ✅ **Responsive Design**: 
  - Mobile: Circular icon-only button (`w-14 h-14 rounded-full`).
  - Desktop: Expanded pill button with label (`md:w-auto md:px-6`).
- ✅ **Interactive**: Subtle scale and shadow lift on hover.
- ✅ **Gradient**: Consistent brand styling.

---

## 🎯 Pattern Decision Matrix

**Which pattern to use?**

| Scenario | Pattern | Why |
|----------|---------|-----|
| Upload files securely | Backend Upload | Credentials safe |
| Display S3 images | Image Proxy | Avoid CORS |
| Guest joins with link | Auto-Join + Loading | Seamless UX |
| New data appears slowly | Polling | Simple, works everywhere |
| Add user without form | Create On-Demand | Lower friction |
| Organize files in S3 | Timestamp + Context | Human readable, unique |
| Expire content | DateTime + Check | Automatic cleanup |

---

## 📌 Quick Copy-Paste Templates

### Template 1: Backend File Upload
```bash
# Files to create:
app/api/upload/route.ts      # Main handler
lib/s3-upload.ts              # S3 utility
lib/s3.ts                     # S3 client

# Environment:
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_S3_BUCKET=...
```

### Template 2: Image Proxy
```bash
# Files to create:
app/api/image/route.ts        # Image proxy

# Usage:
<img src={`/api/image?key=${s3Key}`} />
```

### Template 3: Auto-Join Flow
```bash
# Files to create:
app/auth/join/page.tsx        # Auto-join component

# Must include:
- Suspense wrapper
- useSearchParams hook
- Auto-redirect logic
- Fallback for invalid codes
```

---

## 🔗 Related Patterns

- **Error Handling**: Use consistent 4xx/5xx status codes
- **Caching**: S3 keys with timestamps allow 1-year caching
- **Security**: Whitelist S3 key prefixes in image proxy
- **Performance**: Compress images on upload, cache on proxy
- **Scalability**: Replace polling with WebSocket at 100+ concurrent users

---

**Last Updated**: March 16, 2026  
**Source Project**: Wedding Wall  
**Applicable To**: Any file-upload, gallery, or join-flow app

### Pattern: Disable PWA Zoom (App-Like Feel)
*Source: holeeMonth/APB_LandingPage/index.html*

**Problem**: 
Standard web pages allow pinch-to-zoom, which breaks the "native app" illusion of a PWA and can mess up fixed layouts like FABs or Navbars.

**Solution**: 
Lock the viewport scaling in `layout.tsx` using the `viewport` export (separate from `metadata` in Next.js 14+).

**Implementation**:
```tsx
// app/layout.tsx
import type { Viewport } from "next";

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1.0,
  maximumScale: 1.0,
  userScalable: false,
  // Optional: "cover" extends background to notch/home indicator areas
  viewportFit: "cover", 
};
```

**Why this works:**
1.  `maximumScale: 1.0`: Hard limit on zooming in.
2.  `userScalable: false`: Explicitly disables user gestures for zooming.
3.  `initialScale: 1.0`: Sets the baseline zoom level.
