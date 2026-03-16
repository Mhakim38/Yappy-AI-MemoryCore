# Pattern: Tailwind Bento Grid Layout
**Status:** Proven (Wedding Wall)
**Date:** March 17, 2026
**Type:** Frontend UI / CSS Grid

## Problem
Standard masonry layouts often require complex JS libraries or column-count CSS which breaks logical tab order. Fixed grids leave ugly gaps or crop images poorly.

## Solution
A **Tailwind CSS Grid** with `grid-flow-dense` and smart spanning logic based on content aspect ratio.

### 1. Key Concepts
- **Grid Flow Dense**: `grid-flow-dense` allows items to backfill empty spaces, packing the grid tightly.
- **Aspect Ratio Spanning**:
  - **Landscape (> 1.2)**: Spans 2 columns, 1 row (Wide)
  - **Portrait (< 0.8)**: Spans 1 column, 2 rows (Tall)
  - **Square**: Spans 1 column, 1 row
- **Auto-Detection**: Client-side `onLoad` handler to detect dimensions for legacy/unknown content.

### 2. Implementation

#### The Container
```tsx
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 auto-rows-[250px] grid-flow-dense">
  {items.map((item, idx) => (
    <BentoItem key={item.id} item={item} idx={idx} />
  ))}
</div>
```

#### The Item Component (with Auto-Detect)
```tsx
function BentoItem({ item, idx }: { item: Item; idx: number }) {
  // Initialize with known dimensions or null
  const [dimensions, setDimensions] = useState<{ width: number; height: number } | null>(
    item.width && item.height ? { width: item.width, height: item.height } : null
  );

  let colSpan = 'col-span-1';
  let rowSpan = 'row-span-1';

  if (dimensions) {
    const ratio = dimensions.width / dimensions.height;

    // Logic: Wide items span 2 cols, Tall items span 2 rows
    if (ratio > 1.2) {
      colSpan = 'md:col-span-2';
      rowSpan = 'row-span-1';
    } else if (ratio < 0.8) {
      colSpan = 'col-span-1';
      rowSpan = 'row-span-2';
    }
  }

  return (
    <div
      className={`relative rounded-xl overflow-hidden group shadow-md hover:shadow-xl transition-all duration-300 hover:scale-[1.02] hover:z-10 bg-gray-100 ${colSpan} ${rowSpan}`}
      style={{ animationDelay: `${idx * 0.05}s` }}
    >
      <img
        src={item.url}
        alt={item.title}
        className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
        loading="lazy"
        onLoad={(e) => {
          // Auto-detect dimensions if missing
          if (!dimensions) {
            const img = e.currentTarget;
            if (img.naturalWidth && img.naturalHeight) {
              setDimensions({ width: img.naturalWidth, height: img.naturalHeight });
            }
          }
        }}
      />
    </div>
  );
}
```

### 3. Benefits
- **Responsive**: Easily adjust columns with `md:grid-cols-X`
- **Dense Packing**: No awkward holes in the grid
- **Native CSS**: No heavy masonry libraries
- **Visual Variety**: Breaking the grid makes it feel organic and modern
- **Performance**: Native browser layout engine handles the heavy lifting

### 4. Usage in Wedding Wall
Used in the main gallery (`app/gallery/page.tsx`) to display photos of varying aspect ratios (landscape/portrait uploads) in a cohesive, gap-free wall.
