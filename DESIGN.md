# 📖 UI Design Specifications: Literary Typing Practice

## 1. UI/UX Philosophy
* **Core Principle:** Flat Design, Ultra-Minimalism.
* **Anti-patterns:** NO Glassmorphism, NO heavy shadows, NO complex gradients, NO flashy animations.
* **Focus:** Typographic Art. The text itself is the primary UI element.
* **Eye Care:** Neutral, gentle color palettes designed to prevent eye strain during prolonged reading and typing sessions.

## 2. Visual Specifications

### 2.1. Color Palette (Neutral & Gentle)
* **Background:** Soft Cool Grey/Blue-tinted off-white (`#F4F7F9` or `#EEF2F5`). *Strictly avoid pure white `#FFFFFF`.*
* **Primary Text (Upcoming/Untyped):** Medium Grey (`#64748B` or `#94A3B8`).
* **Typed Text (Correct):** Dark Slate/Charcoal (`#334155` or `#1E293B`). *Strictly avoid pure black `#000000`.*
* **Active Cursor/Highlight:** Subtle, muted yellow block behind the current letter (`#FDF08A` with slight opacity).
* **Error (Wrong typing):** Soft Red background or text (`#FCA5A5`).
* **UI Elements (Icons, minor text):** Faded grey (`#94A3B8`).

### 2.2. Typography (The Soul of the App)
* **Font Family:** 
    * **Primary (Typing text):** Elegant Serif fonts tailored for reading (e.g., *Lora*, *Merriweather*, *Crimson Pro*, or *Literata*).
    * **Secondary (UI elements like stats, timer):** Clean Sans-serif (e.g., *Inter*, *Roboto Mono* for numbers).
* **Font Sizing & Spacing:**
    * Base font size for typing area: `20px` - `24px` for high readability.
    * Line height (Leading): Relaxed, `1.8` to `2.0` to create a book-like appearance and give the text room to breathe.

## 3. Layout Details (Practice View)
The layout must be strictly centered, distraction-free, and artistic.

### 3.1. Top Navigation Bar
* **Left Section:** 
    * "← Quay lại" (Back button).
    * Document Title (e.g., "The Strange Idea That Your Brain Lives in the Past").
    * Meta info: Word/Character count, Rating/Bookmark icon.
* **Right Section:** 
    * Timer (`00:00`).
    * Restart Icon (Loop).
    * Settings Icon (Gear).

### 3.2. Center Area (Typing Zone)
* **Container:** Centered with a maximum width of `800px` - `900px`.
* **Text Display:** Displayed in a solid block of paragraphs, exactly like reading a printed page. 
* **Input Field:** **NO visible input box.** The user types directly over the text body.

## 4. UI States & Typing Mechanics
* **Cursor Tracking:** A soft yellow rectangular highlight always tracks the exact current character the user needs to type.
* **Character States:**
    * `Untyped` -> Medium Grey.
    * `Correct` -> Transitions to Dark Slate.
    * `Incorrect` -> Transitions to Soft Red.
    * `Corrected` (User hits backspace and types correctly) -> Transitions to Dark Slate.
* **Auto-Scrolling:** As the user reaches the bottom of the visible text block, the screen smoothly scrolls down, keeping the active typing line near the vertical center of the screen to maintain visual focus.