# Supabase PostgreSQL + Prisma Pattern
**Level**: 2 (Production-Proven)  
**Source**: Wedding Wall Photo Gallery - Database Layer  
**Status**: Active & Maintained  

---

## Problem Statement
Modern applications need reliable backend databases with:
- Managed PostgreSQL infrastructure
- Real-time subscriptions
- Built-in authentication
- Row-level security (RLS)
- Easy schema management
- Seamless ORM integration

Supabase provides all this without managing servers.

---

## Solution Overview
Complete Supabase setup with Prisma ORM pattern. Provides:
- Supabase PostgreSQL database
- Prisma client for type-safe database access
- Environment configuration
- Schema definition with relationships
- Connection pooling
- Migration management

---

## Implementation

### 1. Supabase Project Setup
```bash
# Step 1: Create Supabase project
# Go to: https://app.supabase.com
# New Project → Choose region (closest to users)
# Wait for provisioning (5-10 min)

# Step 2: Get connection credentials
# Supabase Dashboard → Settings → API
# Copy:
# - Project URL (NEXT_PUBLIC_SUPABASE_URL)
# - Anon Public Key (NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY)
# - Service Role Key (SUPABASE_SERVICE_ROLE_KEY)

# Supabase Dashboard → Databases → Connection pooler
# Copy Connection String:
# - DATABASE_URL (PostgreSQL connection)
```

### 2. Install Dependencies
```bash
npm install @prisma/client prisma @supabase/supabase-js
```

### 3. Environment Configuration (`.env.local`)
```env
# Supabase Configuration
# Get these from: Supabase Dashboard → Settings → API
NEXT_PUBLIC_SUPABASE_URL=https://YOUR_PROJECT_ID.supabase.co
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY=sb_public_YOUR_PUBLIC_KEY
SUPABASE_SERVICE_ROLE_KEY=sb_secret_YOUR_SECRET_KEY
DATABASE_URL=postgresql://postgres:PASSWORD@db.YOUR_PROJECT_ID.supabase.co:5432/postgres

# App Configuration
NEXT_PUBLIC_APP_NAME=Your App
NEXT_PUBLIC_APP_DESCRIPTION=Your app description
```

### 4. Initialize Prisma
```bash
# Initialize Prisma
npx prisma init

# Set DATABASE_URL in .env.local (from Supabase)
# Then generate Prisma client
npx prisma generate
```

### 5. Define Database Schema (`prisma/schema.prisma`)
```prisma
// Prisma schema for your app
// Database: Supabase (PostgreSQL)

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// Example: Wedding photo gallery
model WeddingSession {
  id        String   @id @default(cuid())
  code      String   @unique @db.VarChar(8)
  eventName String
  eventDate DateTime
  createdAt DateTime @default(now())
  expiresAt DateTime

  guests  Guest[]
  photos  Photo[]

  @@index([code])
  @@index([createdAt])
}

model Guest {
  id           String   @id @default(cuid())
  sessionId    String
  name         String
  email        String?
  createdAt    DateTime @default(now())
  lastActivity DateTime @default(now())

  session WeddingSession @relation(fields: [sessionId], references: [id], onDelete: Cascade)
  photos  Photo[]

  @@unique([sessionId, email])
  @@index([sessionId])
}

model Photo {
  id            String   @id @default(cuid())
  sessionId     String
  guestId       String
  title         String?
  description   String?
  s3Url         String
  s3Key         String
  uploadedAt    DateTime @default(now())

  session WeddingSession @relation(fields: [sessionId], references: [id], onDelete: Cascade)
  guest   Guest          @relation(fields: [guestId], references: [id], onDelete: Cascade)

  @@index([sessionId])
  @@index([guestId])
  @@index([uploadedAt])
}

// More models as needed...
```

**Schema Best Practices**:
- Use `@id @default(cuid())` for unique IDs (URL-safe)
- Add `@@index()` for frequently queried fields
- Use `onDelete: Cascade` for related data cleanup
- Include timestamps (`createdAt`, `updatedAt`)
- Define relationships bidirectionally

### 6. Create & Run Migrations
```bash
# Create migration (compares schema to database)
npx prisma migrate dev --name init

# This:
# 1. Creates migration files
# 2. Applies schema to Supabase database
# 3. Generates Prisma client

# For production
npx prisma migrate deploy
```

### 7. Prisma Client Initialization (`lib/prisma.ts`)
```typescript
import { PrismaClient } from '@prisma/client';

const globalForPrisma = global as unknown as { prisma: PrismaClient };

export const prisma =
  globalForPrisma.prisma ||
  new PrismaClient({
    log: ['query'],
  });

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma;
}
```

**Why this pattern**:
- Prevents multiple PrismaClient instances in development
- Single connection pool
- Hot reload friendly

### 8. Database Operations Examples

#### Create Record
```typescript
import { prisma } from '@/lib/prisma';

const guest = await prisma.guest.create({
  data: {
    sessionId: 'session-123',
    name: 'John Doe',
    email: 'john@example.com',
  },
});
```

#### Read with Relations
```typescript
const session = await prisma.weddingSession.findUnique({
  where: { code: 'WED2024' },
  include: {
    guests: true,
    photos: {
      orderBy: { uploadedAt: 'desc' },
      take: 50,
    },
  },
});
```

#### Update with Validation
```typescript
const updated = await prisma.guest.update({
  where: { id: guestId },
  data: {
    lastActivity: new Date(),
  },
});
```

#### Delete with Cascade
```typescript
// Cascades to all related photos and guests
await prisma.weddingSession.delete({
  where: { id: sessionId },
});
```

### 9. API Routes Integration
```typescript
// app/api/guests/route.ts
import { prisma } from '@/lib/prisma';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const sessionId = searchParams.get('sessionId');

  const guests = await prisma.guest.findMany({
    where: { sessionId },
    orderBy: { createdAt: 'desc' },
  });

  return Response.json(guests);
}

export async function POST(request: Request) {
  const body = await request.json();

  const guest = await prisma.guest.create({
    data: {
      sessionId: body.sessionId,
      name: body.name,
      email: body.email,
    },
  });

  return Response.json(guest);
}
```

---

## Adaptation Guide

### For Next.js 16+ (App Router)
1. Create `prisma/schema.prisma`
2. Create `lib/prisma.ts` with singleton pattern
3. Import and use in API routes: `import { prisma } from '@/lib/prisma'`
4. Set `DATABASE_URL` in `.env.local`

### For Next.js Pages Router
Same as above, but import in `pages/api/` routes instead of `app/api/`

### For Node.js Backend
```typescript
import { prisma } from './lib/prisma';

async function main() {
  const data = await prisma.model.findMany();
  console.log(data);
  await prisma.$disconnect();
}

main();
```

### For Express Server
```typescript
import { prisma } from './lib/prisma';

app.get('/api/data', async (req, res) => {
  const data = await prisma.model.findMany();
  res.json(data);
});
```

---

## Configuration Best Practices

| Setting | Recommended | Why |
|---------|-------------|-----|
| Database Region | Closest to users | Lower latency |
| Connection Pooling | Enable | Better resource usage |
| Backup Schedule | Daily | Disaster recovery |
| SSL Mode | Require | Security |
| Network Restrictions | Allowlist IPs | Protection |

---

## Migration Workflow

### Development
```bash
# 1. Update prisma/schema.prisma
# 2. Create migration
npx prisma migrate dev --name describe_change

# 3. Test locally
npm run dev

# 4. Commit migration files to git
```

### Production
```bash
# 1. Review migration files
git log --oneline prisma/migrations/

# 2. Apply in staging first
npx prisma migrate deploy

# 3. Monitor database
# Supabase Dashboard → Database → Slow queries

# 4. Test app
npm run build && npm start
```

---

## Security Considerations

### ✅ Best Practices
- Store DATABASE_URL safely (never in git)
- Use environment variables for all secrets
- Enable Row-Level Security (RLS) policies
- Validate all inputs before database operations
- Use connection pooling for production
- Enable backups in Supabase settings
- Monitor slow queries (Performance tab)

### ❌ Avoid
- Hardcoding database credentials
- Running migrations in production manually
- Exposing SERVICE_ROLE_KEY to frontend
- Trusting user input without validation
- Large N+1 queries without `include`
- Deleting data without backups

---

## Performance Optimization

### Indexing Strategy
```prisma
// Add indexes for:
// 1. WHERE clauses
@@index([sessionId])
@@index([createdAt])

// 2. ORDER BY
@@index([uploadedAt])

// 3. Foreign keys (automatic)
// 4. Unique fields (automatic)
```

### Query Optimization
```typescript
// ❌ Bad: N+1 queries
const sessions = await prisma.weddingSession.findMany();
for (const session of sessions) {
  const photos = await prisma.photo.findMany({
    where: { sessionId: session.id }
  });
}

// ✅ Good: Single query with includes
const sessions = await prisma.weddingSession.findMany({
  include: { photos: true },
});
```

### Pagination
```typescript
const page = 1;
const pageSize = 20;

const photos = await prisma.photo.findMany({
  skip: (page - 1) * pageSize,
  take: pageSize,
  orderBy: { uploadedAt: 'desc' },
});
```

---

## Common Operations

### Session Management
```typescript
// Create session
const session = await prisma.weddingSession.create({
  data: {
    code: 'WED2024',
    eventName: 'John & Jane Wedding',
    eventDate: new Date('2024-06-15'),
    expiresAt: new Date('2024-07-15'),
  },
});

// Get by code
const session = await prisma.weddingSession.findUnique({
  where: { code },
});

// Get with all photos
const session = await prisma.weddingSession.findUnique({
  where: { id },
  include: {
    guests: { select: { id: true, name: true } },
    photos: { orderBy: { uploadedAt: 'desc' }, take: 100 },
  },
});
```

### Guest Management
```typescript
// Create or update
const guest = await prisma.guest.upsert({
  where: { id: guestId },
  update: { lastActivity: new Date() },
  create: {
    sessionId,
    name,
    email,
  },
});

// Count guests
const count = await prisma.guest.count({
  where: { sessionId },
});
```

### Cleanup
```typescript
// Delete old sessions
await prisma.weddingSession.deleteMany({
  where: {
    expiresAt: { lt: new Date() },
  },
});
```

---

## Validation Checklist
- [ ] Supabase project created
- [ ] Connection credentials in `.env.local`
- [ ] Prisma initialized (`npm install @prisma/client prisma`)
- [ ] Schema defined in `prisma/schema.prisma`
- [ ] Migrations created (`npx prisma migrate dev --name init`)
- [ ] Prisma client exported from `lib/prisma.ts`
- [ ] Database operations tested
- [ ] Backups enabled in Supabase
- [ ] Connection pooling enabled
- [ ] Row-level security configured (if needed)

---

## Testing Strategy

```typescript
// Test database connection
async function testConnection() {
  const result = await prisma.$queryRaw`SELECT 1 as test`;
  console.log('✅ Database connected');
}

// Test migrations
async function testMigrations() {
  const tables = await prisma.$queryRaw`
    SELECT table_name FROM information_schema.tables
    WHERE table_schema = 'public'
  `;
  console.log('✅ Tables created:', tables);
}

// Test CRUD
async function testCRUD() {
  // Create
  const guest = await prisma.guest.create({ /* ... */ });
  
  // Read
  const found = await prisma.guest.findUnique({ /* ... */ });
  
  // Update
  await prisma.guest.update({ /* ... */ });
  
  // Delete
  await prisma.guest.delete({ /* ... */ });
  
  console.log('✅ CRUD operations working');
}
```

---

## Troubleshooting

### "Can't reach database server"
- Check DATABASE_URL is correct
- Verify Supabase project is running
- Check firewall/network restrictions
- Try connecting from Supabase dashboard

### "Prisma client not generated"
```bash
npx prisma generate
```

### "Migration failed"
```bash
# Review what would happen
npx prisma migrate resolve --rolled-back init

# Try again
npx prisma migrate dev
```

### "Slow queries"
- Add missing indexes
- Use `include` instead of separate queries
- Check Supabase Performance tab
- Enable query logging: `log: ['query']` in PrismaClient

---

## Future Enhancements
- Implement Row-Level Security (RLS)
- Add caching layer (Redis)
- Set up real-time subscriptions
- Implement audit logging
- Add database monitoring/alerts
- Set up CI/CD migrations

---

## Source Context
- **Maturity**: Production-tested in Wedding Wall (Photo Gallery)
- **Database**: Supabase PostgreSQL (Singapore region)
- **ORM**: Prisma 6.19.2
- **Framework**: Next.js 16+ with App Router
- **Last Updated**: March 16, 2026

**Reuse Status**: ✅ Ready to use in any Next.js, Node.js, or full-stack project needing PostgreSQL.

---

## Decision Checklist

Choose Supabase + Prisma when:
- ✅ Need managed PostgreSQL
- ✅ Want automatic backups
- ✅ Prefer serverless (Vercel, etc)
- ✅ Need real-time capabilities
- ✅ Want type-safe database access
- ✅ Building with Next.js

Skip if:
- ❌ Need non-SQL database (MongoDB, etc)
- ❌ Running on-premise servers
- ❌ No real-time needs
- ❌ Working in language without Prisma support
