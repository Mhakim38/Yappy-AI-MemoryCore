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
