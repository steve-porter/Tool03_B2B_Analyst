# UX Redesign & Brand Compliance - REVISED Implementation Plan

## Revision Summary

**Original Plan Score**: 7/10 (per Claude AI)  
**Revised Plan Score**: 9/10 with incorporated fixes

**Key Changes Based on Claude's Feedback**:
1. ✅ Replace `st.segmented_control` (doesn't exist) with `st.radio(horizontal=True)`
2. ✅ Add complete CSS for segmented control styling
3. ✅ Fix session state initialization logic
4. ✅ Remove redundant mode badge
5. ✅ Move sidebar version info to footer
6. ✅ Use user's preferred mode descriptors

---

## User Decisions (APPROVED)

### Mode Descriptors
- **Sales Mode**: "Sales & Marketing Outreach"
- **Interview Mode**: "Job Interview Prep"

### Mode Toggle UI
- **Horizontal radio buttons** styled as segmented control (not st.segmented_control API)

### Sidebar
- **Remove entirely** (only contained version info, which moves to footer)

### Mode Badge
- **Remove** (redundant with inline toggle above it)

---

## Implementation Changes

### Change 1: Remove Sidebar & Move Version to Footer

**File**: `app.py`

**Delete**: Lines 162-188 (entire sidebar)

**Add to Footer** (after line 281):
```python
st.markdown('<div style="text-align: center; color: #6B7280; font-size: 0.85rem; margin-top: 1rem;">v2.2 Intelligence Platform</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #6B7280; font-size: 0.85rem;"><a href="https://www.linkedin.com/in/stevedporter/" style="color: #6B7280; text-decoration: none;">Built by Somar Intelligence</a></div>', unsafe_allow_html=True)
```

---

### Change 2: Add Inline Mode Toggle

**File**: `app.py`

**Location**: After line 197 (main header), before line 203 (first input)

**Code**:
```python
# Initialize session state for mode
if 'analysis_mode' not in st.session_state:
    st.session_state.analysis_mode = "Sales & Marketing Outreach"

# Mode selector - centered, prominent
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(
        '<p style="text-align: center; color: #C7C9D3; font-size: 0.9rem; '
        'margin-bottom: 0.75rem; font-weight: 500;">Select your intelligence focus:</p>',
        unsafe_allow_html=True
    )
    
    mode_choice = st.radio(
        "Mode",
        options=["Sales & Marketing Outreach", "Job Interview Prep"],
        horizontal=True,
        label_visibility="collapsed",
        index=0 if st.session_state.analysis_mode == "Sales & Marketing Outreach" else 1,
        key="mode_selector"
    )
    
    # Update session state and rerun if changed
    if mode_choice != st.session_state.analysis_mode:
        st.session_state.analysis_mode = mode_choice
        st.rerun()

st.markdown("<br>", unsafe_allow_html=True)
```

---

### Change 3: Remove Mode Badge

**File**: `app.py`

**Delete**: Lines 199-200 (mode badge display)

---

### Change 4: Update Mode Logic

**File**: `app.py`

**Find**: Line 242 (button label logic)
**Replace**:
```python
btn_label = "Generate Strategic Brief" if st.session_state.analysis_mode == "Sales & Marketing Outreach" else "Generate Interview Strategy"
```

**Also update**: Line 211, 247, 255, 267 (anywhere checking mode)

---

### Change 5: Brand Color Compliance

**File**: `app.py` (CSS section)

#### 5a. Update Backgrounds
```css
.stApp {
    background-color: #1C1C2B;  /* was #0F0F17 */
}

.stTextInput input, .stTextArea textarea {
    background-color: #232335 !important;  /* was #161625 */
    border: 1px solid #2F3045 !important;  /* was #374151 */
}

.brief-container {
    background-color: #232335;  /* was #161625 */
    border: 1px solid #2F3045;  /* was #2D2D3F */
}
```

#### 5b. Replace Purple with Cyan
```css
/* Primary CTA Button - solid cyan */
.stButton button {
    background: #22D3EE !important;  /* was purple gradient */
    transition: background 0.3s ease !important;
}

.stButton button:hover {
    background: #06B6D4 !important;
    box-shadow: 0 8px 25px rgba(34, 211, 238, 0.5) !important;
}

/* Input focus states */
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: #22D3EE !important;  /* was #6366F1 */
    box-shadow: 0 0 0 2px rgba(34, 211, 238, 0.2) !important;
}
```

#### 5c. Update Corner Radius
```css
/* Use 18px per brand system */
.stTextInput input, .stTextArea textarea {
    border-radius: 18px !important;  /* was 10px */
}

.stButton button {
    border-radius: 18px !important;  /* was 10px */
}

.brief-container {
    border-radius: 18px !important;  /* was 16px */
}
```

---

### Change 6: Add Segmented Control CSS

**File**: `app.py` (inside `<style>` tag, after line 158)

**Add**:
```css
/* ===== INLINE MODE TOGGLE (SEGMENTED CONTROL) ===== */

/* Container */
div[data-testid="stRadio"][data-baseweb="radio"] {
    background-color: transparent !important;
}

/* Radio group - horizontal with container styling */
div[data-testid="stRadio"] > div[role="radiogroup"] {
    flex-direction: row !important;
    gap: 0 !important;
    justify-content: center !important;
    background-color: #232335 !important;
    border-radius: 18px !important;
    padding: 4px !important;
    border: 1px solid #2F3045 !important;
}

/* Individual radio labels */
div[data-testid="stRadio"] > div[role="radiogroup"] > label {
    flex: 1 !important;
    padding: 0.75rem 2rem !important;
    border: none !important;
    background-color: transparent !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    margin: 0 !important;
    text-align: center !important;
    border-radius: 14px !important;
    color: #C7C9D3 !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
}

/* Hover state */
div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
    background-color: rgba(34, 211, 238, 0.1) !important;
    color: #22D3EE !important;
}

/* Selected state */
div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
    background-color: #22D3EE !important;
    color: #1C1C2B !important;
    font-weight: 600 !important;
    box-shadow: 0 2px 8px rgba(34, 211, 238, 0.3) !important;
}

/* Hide radio circles */
div[data-testid="stRadio"] input[type="radio"] {
    display: none !important;
}

/* Mobile adjustments */
@media (max-width: 768px) {
    div[data-testid="stRadio"] > div[role="radiogroup"] > label {
        padding: 0.65rem 1.5rem !important;
        font-size: 0.9rem !important;
    }
}
```

---

### Change 7: Remove Sidebar CSS

**File**: `app.py`

**Delete**: Lines 35-79 (all sidebar-related CSS)

---

## QA Testing Plan

### Test Case 1: Mode Toggle (Desktop)
**Steps**:
1. Load app on desktop
2. Verify mode toggle is centered below header
3. Click "Job Interview Prep"
4. Verify inputs change to JD + CV fields

**Pass Criteria**:
- ✅ Toggle visible and styled as segmented control
- ✅ Cyan highlight on selected mode
- ✅ Form updates correctly

### Test Case 2: Mode Toggle (Mobile)
**Steps**:
1. Load app on mobile device (or Chrome DevTools 390x844)
2. Verify mode toggle is visible (no hamburger menu needed)
3. Tap "Job Interview Prep"
4. Verify inputs change

**Pass Criteria**:
- ✅ Toggle visible without sidebar
- ✅ Touch targets are adequate (44px minimum)
- ✅ Mode changes persist

### Test Case 3: Brand Color Compliance
**Steps**:
1. Inspect all elements visually
2. Check with DevTools color picker

**Pass Criteria**:
- ✅ Background: `#1C1C2B`
- ✅ Panels: `#232335`
- ✅ Borders: `#2F3045`
- ✅ Accent: `#22D3EE` (no purple)
- ✅ Corner radius: 18px

### Test Case 4: Session State Persistence
**Steps**:
1. Select "Job Interview Prep"
2. Enter URL, JD, upload CV
3. Generate report
4. Verify mode didn't reset

**Pass Criteria**:
- ✅ Mode stays selected after generation
- ✅ No unexpected resets

### Test Case 5: Sales Mode End-to-End
**Steps**:
1. Select "Sales & Marketing Outreach"
2. Enter URL + solution description
3. Click "Generate Strategic Brief"

**Pass Criteria**:
- ✅ Correct inputs displayed
- ✅ Button label correct
- ✅ Report generates successfully

### Test Case 6: Interview Mode End-to-End
**Steps**:
1. Select "Job Interview Prep"
2. Enter URL + JD + CV
3. Click "Generate Interview Strategy"

**Pass Criteria**:
- ✅ Correct inputs displayed
- ✅ Button label correct
- ✅ Report generates successfully

---

## Implementation Checklist

- [ ] Remove sidebar (lines 162-188)
- [ ] Add inline mode toggle after header
- [ ] Add segmented control CSS
- [ ] Remove mode badge (lines 199-200)
- [ ] Update background colors (3 places)
- [ ] Update accent colors (purple → cyan, 5 places)
- [ ] Update border colors (3 places)
- [ ] Update corner radius (18px, 4 places)
- [ ] Remove sidebar CSS (lines 35-79)
- [ ] Move version to footer
- [ ] Update mode logic throughout
- [ ] Test all 6 test cases
- [ ] Capture before/after screenshots

---

## Expected Visual Result

**Layout Flow**:
```
┌─────────────────────────────────────┐
│  Company Intelligence Platform      │
└─────────────────────────────────────┘
         
┌─────────────────────────────────────┐
│ Select your intelligence focus:     │
│ ┌──────────────┬─────────────────┐ │
│ │   Sales      │  Job Interview  │ │
│ │ & Marketing  │      Prep       │ │
│ │  Outreach    │                 │ │
│ │ (SELECTED)   │                 │ │
│ └──────────────┴─────────────────┘ │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 1. Target Company                   │
│ [Input field - cyan focus]          │
│                                     │
│ 2. My Solution                      │
│ [Text area - cyan focus]            │
│                                     │
│ [Generate Strategic Brief]          │
│      (Cyan button)                  │
└─────────────────────────────────────┘

        v2.2 Intelligence Platform
        Built by Somar Intelligence
```

---

## Brand Compliance Verification

After implementation, verify all colors match `somar_brand_colour_style_system.md`:

- [ ] Primary background: `#1C1C2B`
- [ ] Panel/surface: `#232335`  
- [ ] Borders: `#2F3045`
- [ ] Primary accent: `#22D3EE` (cyan)
- [ ] Hover state: `#06B6D4` (darker cyan)
- [ ] No purple (`#6366F1`) anywhere
- [ ] Corner radius: 18px
- [ ] Font: Inter throughout

---

## Timeline

- **Implementation**: 45 minutes
- **QA testing**: 30 minutes
- **Screenshot documentation**: 15 minutes
- **Total**: ~1.5 hours

---

## Ready to Implement

All Claude AI feedback incorporated. User decisions confirmed. Proceeding to execution phase.
