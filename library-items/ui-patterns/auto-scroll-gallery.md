# Auto-Scroll Gallery Pattern

## Overview
Horizontal marquee/carousel effect that auto-scrolls photos infinitely. Toggleable between grid and auto-scroll views.

## State Management
```typescript
const [viewMode, setViewMode] = useState<'grid' | 'marquee'>('grid');
```

## Container Styling (Tailwind)
```typescript
const containerClass = mode === 'marquee' 
  ? "relative rounded-xl overflow-hidden group shadow-md hover:shadow-xl transition-all duration-300 w-[300px] h-[400px] flex-shrink-0 mx-2"
  : `relative rounded-xl overflow-hidden group shadow-md hover:shadow-xl transition-all duration-300 hover:scale-[1.02] hover:z-10 bg-gray-100 dark:bg-gray-800 ${colSpan} ${rowSpan}`;
```

## Render Pattern
```tsx
{viewMode === 'marquee' ? (
  <div className="w-full overflow-hidden py-10">
    <div className="animate-marquee-left">
      {/* Double the list for seamless loop */}
      {[...photos, ...photos].map((photo, idx) => (
        <GalleryItem key={`${photo.id}-${idx}`} photo={photo} idx={idx} mode="marquee" />
      ))}
    </div>
  </div>
) : (
  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 auto-rows-[250px] grid-flow-dense">
    {photos.map((photo, idx) => (
      <GalleryItem key={photo.id} photo={photo} idx={idx} mode="grid" />
    ))}
  </div>
)}
```

## Toggle Button
```tsx
{photos.length > 5 && (
  <button
    onClick={() => setViewMode(viewMode === 'grid' ? 'marquee' : 'grid')}
    className="mt-2 flex items-center gap-2 px-4 py-2 bg-white dark:bg-gray-800 rounded-full shadow-sm border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
  >
    <FontAwesomeIcon 
      icon={viewMode === 'grid' ? faPlay : faTableCells} 
      className="w-4 h-4 text-orange-500" 
    />
    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
      {viewMode === 'grid' ? 'Auto-Scroll' : 'Grid View'}
    </span>
  </button>
)}
```

## CSS Animation Required
Add to your global CSS or Tailwind config:
```css
@keyframes marquee-left {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

.animate-marquee-left {
  animation: marquee-left 30s linear infinite;
  display: flex;
}
```

## Dependencies
- `@fortawesome/react-fontawesome` for icons
- `tailwindcss` for styling
- Photos array with id, guest.name, uploadedAt properties
