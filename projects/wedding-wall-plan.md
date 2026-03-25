# Wedding Wall Features Implementation Plan

## Problem Statement
The Wedding Wall app needs 6 key enhancements based on user feedback to improve usability during events:
1. **Persistent Name**: Remember guest name after first upload.
2. **Image Compression**: Client-side compression to fix large file upload issues.
3. **Wedding Header**: Display "Selamat Datang ke [Couple] Wedding" dynamically.
4. **Auto-Scroll Gallery**: Marquee/auto-scroll mode when photos > 5.
5. **Money Gift QR**: Admin-uploaded QR code for money gifts (Angpao).
6. **QR Code & Expiration**: QR for wedding code, valid for 48 hours.

## Implementation Steps

### Phase 1: Quick Wins (Frontend)
- [x] **Persistent Name**: Update `app/gallery/upload/page.tsx` to use `localStorage`.
- [ ] **Wedding Header**: Update `app/gallery/page.tsx` to show `eventName`.
- [ ] **Image Compression**: 
    - Install `browser-image-compression`.
    - Update `app/gallery/upload/page.tsx` to compress before upload.

### Phase 2: Gallery Experience
- [ ] **Auto-Scroll**: ❌ **CANCELLED** (User preference: Dislikes marquee)
- [ ] **Infinite Scroll / Lazy Loading**: ✅ **COMPLETED** (Mar 25, 2026)
    - **Backend**: Added `page` and `limit` to `app/api/photos/route.ts`.
    - **Frontend**: Implemented infinite scroll with auto-fetching and deduplication.
- [ ] **QR Code Display**:
    - Install `qrcode`.
    - Update `app/gallery/page.tsx` to generate/display QR for the current session URL.

### Phase 3: Backend & Admin (Complex)
- [ ] **Database Schema**:
    - Add fields to `WeddingSession`: `giftQrUrl`, `giftQrKey`, `giftMessage`.
    - Run migration.
- [ ] **Money Gift Feature**:
    - Create API `api/admin/upload-gift-qr`.
    - Create UI `components/GiftModal.tsx`.
    - Add "Send Gift" button in Gallery.
- [ ] **Admin Page** (New):
    - Create `app/admin/page.tsx` to manage sessions & upload gift QRs.

## Notes
- `browser-image-compression` settings: max 1920px, 0.8 quality.
- Auto-scroll should pause on hover/tap.
- QR code should encode the full URL `https://.../?code=XYZ`.
