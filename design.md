---
version: alpha
name: Zendesk Bright System
description: A clean, editorial light-mode system with a bold lime accent and minimal chrome.
colors:
  primary: "#D1F470"
  secondary: "#11110D"
  tertiary: "#000000"
  neutral: "#FFFFFF"
  surface: "#F7F7F5"
  on-surface: "#000000"
  error: "#D92D20"
  border: "#E5E7EB"
  muted: "#6B7280"
  overlay: "#11110D"
typography:
  headline-display:
    fontFamily: Vanilla Sans
    fontSize: 51px
    fontWeight: 700
    lineHeight: 61px
    letterSpacing: 0.75px
  headline-lg:
    fontFamily: Vanilla Sans
    fontSize: 38px
    fontWeight: 500
    lineHeight: 53.55px
    letterSpacing: 0px
  headline-md:
    fontFamily: Vanilla Sans
    fontSize: 28px
    fontWeight: 500
    lineHeight: 28.75px
    letterSpacing: 0px
  headline-sm:
    fontFamily: Vanilla Sans
    fontSize: 20px
    fontWeight: 500
    lineHeight: 21.75px
    letterSpacing: 0px
  body-lg:
    fontFamily: Vanilla Sans
    fontSize: 18px
    fontWeight: 400
    lineHeight: 26px
    letterSpacing: 0px
  body-md:
    fontFamily: Vanilla Sans
    fontSize: 15px
    fontWeight: 400
    lineHeight: 21.75px
    letterSpacing: 0px
  body-sm:
    fontFamily: Vanilla Sans
    fontSize: 13px
    fontWeight: 400
    lineHeight: 18px
    letterSpacing: 0px
  label-lg:
    fontFamily: Vanilla Sans
    fontSize: 18px
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: 0px
  label-md:
    fontFamily: Vanilla Sans
    fontSize: 15px
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: 0px
  label-sm:
    fontFamily: Vanilla Sans
    fontSize: 13px
    fontWeight: 500
    lineHeight: 1.2
    letterSpacing: 0px
  overline:
    fontFamily: Vanilla Sans
    fontSize: 13px
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: 0.02em
rounded:
  none: 0px
  sm: 4px
  md: 8px
  lg: 16px
  xl: 24px
  full: 9999px
spacing:
  xs: 2px
  sm: 12px
  md: 20px
  lg: 32px
  xl: 76px
  gutter: 24px
  margin: 32px
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.secondary}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.lg}"
    padding: 10px 20px
    height: 40px
  button-primary-hover:
    backgroundColor: "#C3E85F"
    textColor: "{colors.secondary}"
    rounded: "{rounded.lg}"
  button-secondary:
    backgroundColor: "transparent"
    textColor: "{colors.tertiary}"
    typography: "{typography.label-lg}"
    rounded: "{rounded.sm}"
    padding: 10px 20px
    height: 40px
  button-tertiary:
    backgroundColor: "transparent"
    textColor: "{colors.neutral}"
    typography: "{typography.body-sm}"
    rounded: "{rounded.none}"
    padding: 0px
  card:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.tertiary}"
    rounded: "{rounded.md}"
    padding: 16px
  input:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.tertiary}"
    typography: "{typography.body-md}"
    rounded: "{rounded.md}"
    padding: 12px 16px
    height: 48px
  pill:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.tertiary}"
    typography: "{typography.label-sm}"
    rounded: "{rounded.full}"
    padding: 8px 14px
---

# Zendesk Bright System

## Overview
Zendesk presents a polished, high-clarity enterprise brand with a friendly edge. The overall tone is professional and confident, but the bright lime accent and spacious hero imagery add energy and approachability. The experience feels editorial and conversion-focused: minimal chrome, strong headline hierarchy, and prominent calls to action.

## Colors
- **Primary (#D1F470):** A vivid lime accent used for the main conversion button and key emphasis. It brings optimism and immediacy without feeling neon.
- **Secondary (#11110D):** A soft near-black used for strong contrast on primary buttons and for dark promotional bars. It reads as warmer than pure black.
- **Tertiary (#000000):** Pure black used for body text, navigation, and outlines where maximum clarity is needed.
- **Neutral (#FFFFFF):** Clean white used for the page background, cards, form fields, and negative space throughout the interface.
- **Surface (#F7F7F5):** A subtle off-white surface tone for gentle separation when a section needs a quieter layer than pure white.
- **Border (#E5E7EB):** A light cool gray for hairline dividers, card edges, and input borders.
- **Muted (#6B7280):** A restrained gray for secondary utility text and de-emphasized metadata.
- **Overlay (#11110D):** A dark overlay tone for announcement bars and dark UI strips where content must stand apart from the bright page.
- **Error (#D92D20):** A reserved red for validation and destructive feedback; it should remain rare in a system this calm.

## Typography
The system uses Vanilla Sans across the interface, creating a unified, modern voice that feels crisp rather than ornamental. Headlines range from 51px down to 20px, with medium to bold weights for strong hierarchy; the hero headline uses a slightly tighter, more assertive feel with 700 weight and modest positive letter spacing. Body copy is compact and highly legible at 15px and 18px, supporting a dense amount of marketing information without visual clutter.

Labels and buttons lean semibold, which helps CTAs read clearly at a glance. Uppercase treatment appears in small promotional labels such as the hero kicker, and those all-caps words are spaced and weighted to feel authoritative rather than decorative.

## Layout
The layout is centered around a wide, fluid marketing container with generous horizontal breathing room and very strong top-to-bottom hierarchy. The page uses large section spacing, especially in the hero, where content is anchored left while imagery occupies the opposite side. Rhythm is driven by the observed spacing scale: tight 2px separators, practical 12px and 20px gaps, then larger 32px and 76px jumps for section breathing room and campaign blocks.

Components inside forms and nav areas keep padding compact, while hero content is stacked with clear vertical separation between kicker, headline, paragraph, trust note, and CTA row. The result is spacious but efficient, designed for quick scanning and fast conversion.

## Elevation & Depth
The design is intentionally flat in terms of shadows; hierarchy comes from color contrast, whitespace, and large visual assets rather than depth effects. Hairline borders and subtle tonal changes define edges when needed, especially in the navigation and form fields. The main hero image and the dark promotional strip do most of the heavy lifting for depth through tonal contrast rather than cast shadows.

## Shapes
The shape language is soft and approachable, with a notable preference for rounded corners on primary interactive elements. Primary buttons feel pill-like with 16px radius, while cards and inputs stay slightly more restrained with 8px to 4px corners. Overall, the system balances warmth and utility: friendly enough for consumer-facing marketing, but still disciplined for enterprise use.

## Components
Buttons are the clearest expression of the brand. `button-primary` uses the lime `primary` fill, dark text, strong semibold labeling, and a 16px radius; it should remain the dominant CTA style. `button-secondary` is a transparent outlined control with black text and a square-leaning 4px radius, suited to alternate actions like “View demo.” `button-tertiary` is a link-like treatment for lightweight navigation or utility actions, especially in dark promotional bars.

Cards should use the `card` treatment: white background, 1px light border, modest padding, and no shadow. Keep cards calm and content-led; avoid decorative elevation. Inputs should follow the `input` pattern with white fill, subtle border, 48px height, and comfortable internal padding for fast form completion.

Pills and compact tags should use the `pill` style: full rounding, restrained padding, and small typography. This is appropriate for short labels, status chips, and trust indicators. Navigation items should remain text-first and understated, with dropdown indicators kept subtle and aligned to the system’s minimal tone.

## Do's and Don'ts
- Do keep primary CTAs in the lime accent so the conversion path is immediately obvious.
- Do use Vanilla Sans consistently for all UI text to preserve the brand’s unified voice.
- Do rely on whitespace, color contrast, and hierarchy instead of shadows or heavy surface effects.
- Do keep borders thin and neutral so form fields and cards feel clean, not boxed in.
- Don't introduce saturated secondary colors that compete with the primary lime accent.
- Don't add deep shadows, gradients, or glossy effects; the system should stay flat and modern.
- Don't over-round every component; reserve the fullest curves for pills and the main primary button.
- Don't let body copy grow too large or too loose, or the marketing layout will lose its crisp, conversion-focused rhythm.