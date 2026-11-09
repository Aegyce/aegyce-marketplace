# 影棚肖像提示词模板

## 使用方法

先按 `SKILL.md` 确认原照、样式图和摄影参考各自的职责。将下方占位符替换为实际值；没有某类图片时，删除相应说明并重新编号。不要把所有图片都笼统称作参考图。

建议参数：

| 占位符 | 说明 |
| --- | --- |
| `{{ORIGINAL}}` | 用户原照在图像工具中的编号，例如 Image 1 |
| `{{STYLE}}` | 当前认可版本或随附风格样图的编号，例如 Image 2 |
| `{{PHOTO_REFERENCE}}` | 可选摄影参考图编号；没有则删除 |
| `{{OUTFIT}}` | 用户明确要求的衣服，默认优质炭灰西服、白衬衫、深蓝领带 |
| `{{BACKGROUND}}` | 用户指定背景，默认低饱和深蓝灰渐变 |
| `{{RATIO}}` | 参考图实测或用户明确要求的比例，默认 20:23 |
| `{{PIXEL_TARGET}}` | 可选输出像素目标，例如 1920 × 2208；不构成已达成规格 |
| `{{CURRENT_CORRECTION}}` | 本轮要改的问题；首次制作写完整目标 |

## 完整模板

```text
Create a high-fidelity photographic edit of {{ORIGINAL}}, the user's ORIGINAL photograph.

INPUT ROLES
- {{ORIGINAL}} is the sole authoritative source for the person's identity, exact facial geometry, natural expression, hairstyle, body proportions and real facial detail.
- {{STYLE}} supplies ONLY the chosen clothing, background, framing and overall style. Do not copy degraded, blurred or reinterpreted facial details from a previous generated image. If this style image depicts someone else, never borrow that person's face or identity.
- {{PHOTO_REFERENCE}} supplies ONLY the requested photographic styling or backdrop. Never transfer that other person's identity, pose or features.

TASK
{{CURRENT_CORRECTION}}
Use the original photo to establish the person. Use the explicitly assigned references to establish the style. Keep already accepted elements unless this task requires changing them.

IDENTITY AND FACIAL DETAIL
Preserve the exact original eye shapes, eyelids, eyebrows, nose, lips, ears, jaw, expression, hairline, hairstyle and natural proportions. Retain real photographic detail in eyes, lashes, individual brow hairs, nostril and lip edges. Keep youthful or mature skin as it actually appears in the original; do not change apparent age.
Make the face cleanly focused, not blurry or airbrushed. Keep natural smooth skin with delicate real detail, not coarse invented pores, stippling, wrinkles, wavy texture or exaggerated stubble. Avoid both waxy smoothing and aggressive sharpening. No halos or plastic skin. Do not change the face merely to make it look more symmetrical or idealized.
Keep the eyes naturally engaged through small plausible catchlights and readable iris detail. Do not enlarge the eyes, pupils or irises, bleach the whites, change eye color, or add decorative sparkle.

COHERENT STUDIO LIGHTING
Use one credible commercial studio lighting setup for the whole person. A large double-diffused softbox about 30 degrees camera-left and slightly above eye level provides the key. A softer near-camera fill about one stop weaker preserves detail in shadow. Form a short soft nose shadow, gradual cheek modeling and a natural chin shadow continuing into the neck and collar. Let the shoulders and lapels follow that same light direction. Keep realistic catchlights consistent with the key.
Use neutral daylight studio color, healthy natural skin, controlled highlights and gentle continuous tonal transitions. The face must not look pasted onto the torso, overbright, orange, chalky or flat. Preserve facial geometry while allowing coherent changes to illumination.

WARDROBE
{{OUTFIT}}
Convey quality through a well-fitting shoulder line, clean sleeve heads, dimensional rolled lapels, natural drape and subtle fine fabric weave. Use restrained fabric highlights; avoid plastic shine, exaggerated repeated patterns and invented embossed texture. Make the collar fit the original neck and use believable contact shadows. Do not add jewelry, badges, logos or accessories without a request.

BACKGROUND AND DEPTH
{{BACKGROUND}}
Use a broad low-saturation gradient with a muted slate-blue central region and deeper navy periphery. Keep background details quiet and soft, as a backdrop well behind the subject. Separate the person through coherent tonal relationships and natural depth, not a bright circle around the head. Avoid saturated royal blue, harsh vignette edges, sharp wall texture or obvious cloud patterns.

FOCUS AND FRAMING
Aim for clean, high-definition commercial portrait photography: focus on the eyes with enough depth of field for the entire face. The face must resolve at least as clearly as the tie and lapels. The distant background alone may be softer. An f/8, low-ISO studio look is a visual target, not metadata to add.
Output a {{RATIO}} portrait canvas, with {{PIXEL_TARGET}} as the requested target where supported. Preserve natural head-to-body proportions, comfortable headroom and the requested pose. Reframe the canvas rather than stretch the person. Do not copy a reference person's seated or angled pose unless asked.

Deliver one photorealistic result. No text, frame, watermark or extra objects.
```

## 精简的局部修正追加语句

仅在当前图像身份与细节完好时使用局部迭代；所有迭代继续提供原照作人物依据。

### 面部模糊

```text
Return to the original photo for facial detail. Restore clear eyes, lashes, brows, nostril and lip edges. Do not sharpen the blurred generated face or invent skin detail. Use the accepted version only for wardrobe, background and composition. Keep natural fine skin and coherent studio lighting.
```

### 面部粗糙

```text
Remove artificial grain, excessive pore contrast and wavy skin texture. Match the original photo's natural skin softness. Preserve crisp eyes, brows and lip boundaries, and preserve the existing three-dimensional lighting. Do not globally blur or brighten the face.
```

### 眼神需要更有神

```text
Make a restrained local eye retouch: small coherent softbox catchlights, clear natural iris detail and gently balanced eyelid shadows. Preserve eye shape, size, gaze, eye color and pupil size. Keep the rest of the accepted portrait unchanged as closely as the tool permits.
```

### 脸与身体衔接突兀

```text
Unify the light across the face, neck, collar, shoulders and lapels. Preserve identity, but allow lighting changes. Align nose, jaw and collar shadows with one soft key light, match skin color from face to neck, and control face exposure. Do not preserve contradictory flat face lighting from an earlier version.
```
