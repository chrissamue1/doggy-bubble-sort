# 🐶 BUBBLE SORT — Pup Edition

A visual, 3D isometric educational sorting simulation built with Python and Pygame, inspired by the iconic **Algomaster** dark-mode visualizer!

Featuring **Spider-Pup**, an upside-down superhero dog hanging from a ceiling web/leash, dynamically aiming targeting beams and pulling adjacent 3D dog breed blocks into the air to swap them.

---

## 📸 Visual Showcase

- **Hero Character**: Upside-down superhero dog hanging from the ceiling on a silver leash with glowing paw targeting rings.
- **Dynamic Leashes**: Taut glowing lines extending from Spider-Pup's paws down to the two active comparing blocks.
- **3D Isometric Columns**: Real-time pseudo-3D blocks with top-cap numbers, front faces with breed names & weights, and proportional heights based on actual dog weights (2kg to 60kg).
- **Dark Mode Aesthetic**:
  - Unsorted blocks: Matte slate-grey (`2, 3, 1`)
  - Left active block: Vibrant Glowing Orange (`5`)
  - Right active block: Electric Azure Cyan (`4`)
  - Sorted blocks: Luminous Emerald Green (`6, 7, 8`)
- **Terminal Code Callout**: Monospace syntax highlighting at the bottom (`compare a[j], a[j+1]`, `swap a[j], a[j+1]`).

---

## 🐕 Dog Breeds & Numeric Values

| Value | Breed | Weight | Height Rank |
| :---: | :--- | :---: | :---: |
| **#1** | **Chihuahua** | **2 kg** | 1 (Shortest) |
| **#2** | **Pomeranian** | **3 kg** | 2 |
| **#3** | **Pug** | **8 kg** | 3 |
| **#4** | **French Bulldog** | **12 kg** | 4 |
| **#5** | **Corgi** | **14 kg** | 5 |
| **#6** | **Beagle** | **15 kg** | 6 |
| **#7** | **Border Collie** | **20 kg** | 7 |
| **#8** | **Golden Retriever** | **30 kg** | 8 |
| **#9** | **German Shepherd** | **35 kg** | 9 |
| **#10** | **Great Dane** | **60 kg** | 10 (Tallest) |

---

## 🚀 How to Run

From the project directory:

```powershell
cd C:\Users\cr7ch\.gemini\antigravity\scratch\dog-bubble-sort
python main.py
```

### Automated Headless Verification

```powershell
python main.py --test
```

---

## ⌨️ Controls & Shortcuts

| Action | Shortcut | UI Button |
| :--- | :---: | :--- |
| **Play / Pause** | `Space` | `> Play Sort` / `\|\| Pause` |
| **Step Forward** | `Right Arrow` | `Next >` |
| **Step Backward** | `Left Arrow` | `< Prev` |
| **Reset** | `R` | `Reset` |
| **Shuffle Pack** | `S` | `Shuffle Pack` |
| **Speed Slider** | Mouse Drag | `0.4x` to `3.5x` |
| **Dog Count** | Click Button | Cycle `5`, `6`, `8`, or `10` dogs |
| **Sort Order** | Click Button | `Order: Ascending` / `Descending` |
| **Sound Toggle** | `M` | `Sound: ON` / `OFF` |
