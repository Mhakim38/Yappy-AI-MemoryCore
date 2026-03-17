# 📚 Pattern Library Index

**How to Use This Library:**
1. Look up the problem/scenario you're facing
2. Find the matching pattern
3. Copy the code template
4. Adapt to your project

---

## 🔍 Quick Problem Lookup

### "I need to upload files to S3"
→ **Pattern: Backend File Upload** (p. 2)
- Safe, secure, server-side
- No CORS issues
- Can add validation/processing

### "Images from S3 won't display (CORS error)"
→ **Pattern: Image Proxy** (p. 3)
- Create `/api/image` endpoint
- Proxy all S3 requests through backend
- Enables caching + security

### "Guest gets invite link but doesn't auto-join"
→ **Pattern: URL Code Auto-Join** (p. 6)
- Detect code in URL params
- Validate silently
- Auto-redirect with loading screen
- Use Suspense boundary

### "New photos don't appear instantly"
→ **Pattern: Polling for New Data** (p. 9)
- Poll backend every 3-5 seconds
- Simple, works everywhere
- Good for < 100 concurrent users

### "I have foreign key constraint errors"
→ **Pattern: Guest Creation On-Demand** (p. 8)
- Create users during first action
- Avoid pre-registration step
- Prevents missing references

### "S3 files are disorganized"
→ **Pattern: S3 Key Generation** (p. 12)
- Use: `{category}/{context}/{timestamp}-{identifier}-{filename}`
- Example: `photos/session-123/1710657600000-john-wedding.jpg`
- Prevents collisions, human readable

### "Sessions need to expire"
→ **Pattern: Session with Expiry** (p. 14)
- Use DateTime field
- Check on every request
- Return 410 Gone for expired

### "Form is laggy, no feedback"
→ **Pattern: Form with Loading State** (p. 17)
- Track: loading, error, success states
- Disable button while processing
- Show error messages
- Redirect on success

### "Gallery layout is broken on mobile"
→ **Pattern: Masonry Gallery Layout** (p. 19)
- Use Tailwind `columns-{1,2,3}`
- Works responsive
- Clean, simple CSS

### "Mobile menu transition is jumpy"
→ **Pattern: Glassmorphic Responsive Navbar** (p. 20)
- Includes **Smooth Mobile Menu Transition**
- Animate `max-height` & `opacity`
- No layout shifts or gaps

### "Copy to clipboard fails on mobile/PWA"
→ **Pattern: Robust Clipboard Copy** (p. 21)
- Fallback for non-secure contexts
- Uses `document.execCommand` hidden textarea
- Essential for local testing/PWA

### "Text colors look wrong/grey in light mode"
→ **Pattern: Handling Global CSS Conflicts** (p. 22)
- Global `p` tags in `globals.css` override Tailwind
- Use explicit classes `text-gray-900`
- Check `foreground` variable definitions

---

## 📊 Pattern Categories

| Category | Patterns | When to Use |
|----------|----------|-------------|
| **File Uploads** | Backend Upload | Always for S3 |
| **Image Display** | Image Proxy | S3 + browsers |
| **User Join** | Auto-Join + Loading | Invite links |
| **Real-time** | Polling | < 100 users |
| **Database** | Expiry, On-Demand Creation | Session/Guest mgmt |
| **S3 Organization** | Key Generation | File organization |
| **UI/UX** | Forms, Galleries, Navbar, CSS Fixes | User interaction |
| **Integration** | Robust Clipboard | PWA/Mobile features |

---

## 🎯 Common Scenarios

### Scenario: Build a Photo Gallery App
**Use Patterns:**
1. Backend File Upload (for uploading)
2. Image Proxy (for displaying)
3. Polling (for new photos)
4. Masonry Gallery (for layout)
5. Form with Loading State (for uploads)

### Scenario: Build an Invite-Only Event App
**Use Patterns:**
1. URL Code Auto-Join (seamless entry)
2. Session with Expiry (auto-cleanup)
3. Guest Creation On-Demand (low friction)

### Scenario: Build a Real-time Chat App
**DON'T use:** Polling (too slow)  
**USE instead:** WebSocket (out of scope for this library)

---

## 💾 Files in Pattern Library

| File | Purpose |
|------|---------|
| `PATTERN_LIBRARY.md` | Full patterns with code examples |
| `PATTERNS_INDEX.md` | This file - quick lookup |
| `DECISION_MATRIX.md` | Help choosing between patterns |

---

## 🔗 Cross-References

**Related to Backend Upload:**
- Secure S3 Credentials (p. 11)
- Error Handling Best Practices
- File Validation

**Related to Image Proxy:**
- S3 Key Generation (p. 12)
- Caching Strategy
- Security Whitelisting

**Related to Auto-Join:**
- Session Validation
- Fallback Handling
- Loading States

---

## 📈 When to Evolve Patterns

### From Polling → WebSocket
**When:**
- > 100 concurrent users
- Need < 1 sec latency
- Can manage infrastructure

**How:**
- Use Socket.io or ws library
- Maintain open connections
- Broadcast on new data

### From Backend Upload → Direct Upload
**When:**
- > 1GB file sizes
- High upload volume
- Server cost is issue

**How:**
- Use pre-signed URLs
- Configure S3 CORS
- Accept security tradeoffs

### From Single Server → Distributed
**When:**
- > 10,000 concurrent users
- Need 99.9% uptime
- Have scaling budget

**How:**
- Add load balancer
- Use managed databases
- Implement CDN for images

---

**Created**: March 16, 2026  
**Source**: Wedding Wall Project  
**Maintainer**: Yappy (AI Assistant)
