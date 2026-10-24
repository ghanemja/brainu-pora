// Splatform (formerly art-medium) — SVG filter defs + helpers.
// The CSS references these filters by id (filter: url(#am-watercolor)), so they
// must exist in the document. Importing this module installs them once.

export const MEDIUMS = ['watercolor', 'acrylic', 'charcoal', 'paper', 'marker'];
export const THEMES = ['light', 'dark', 'auto'];
/** Styles of the acrylic medium. Impasto is the default. */
/** Styles per medium. The first one is the default. */
export const MEDIUM_STYLES = {
  acrylic: ['impasto', 'impressionist', 'realism'],
  charcoal: ['newsprint', 'sketchbook', 'kraft'],
  marker: ['plain', 'notebook', 'parchment'],
};
export const STYLES = Object.values(MEDIUM_STYLES).flat();

const FILTERS = `
<svg id="am-filters" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false"
     style="position:absolute;width:0;height:0;overflow:hidden">
  <defs>
    <!-- Watercolor: bleeding edges, pigment granulation, darker pooled rim -->
    <filter id="am-watercolor" x="-25%" y="-25%" width="150%" height="150%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="4" seed="3" result="noise"/>
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="14" xChannelSelector="R" yChannelSelector="G" result="bled"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.75" numOctaves="2" seed="7" result="grain"/>
      <feColorMatrix in="grain" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0.9 0 0 0 0.3" result="grainAlpha"/>
      <feComposite in="bled" in2="grainAlpha" operator="in" result="granulated"/>
      <feMorphology in="bled" operator="erode" radius="3" result="inner"/>
      <feGaussianBlur in="inner" stdDeviation="3" result="innerSoft"/>
      <feComposite in="bled" in2="innerSoft" operator="out" result="rim"/>
      <feMerge><feMergeNode in="granulated"/><feMergeNode in="rim"/></feMerge>
    </filter>
    <filter id="am-watercolor-stroke" x="-10%" y="-200%" width="120%" height="500%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="3" seed="4" result="noise"/>
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="5" xChannelSelector="R" yChannelSelector="G" result="bled"/>
      <feGaussianBlur in="bled" stdDeviation="0.4"/>
    </filter>

    <!-- Acrylic: thick broken-color impasto. Horizontal band noise drags the
         paint into short directional strokes and staggers their ends along
         the edge. A posterized noise field splits the paint into hard-edged
         dabs: some hue-shifted cooler or warmer, some lighter or darker, so
         no area is one flat color. The dabs' values (plus bristle grooves)
         become a height map, lit for ridges and a little gloss. -->
    <filter id="am-acrylic" x="-8%" y="-20%" width="116%" height="145%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.016 0.13" numOctaves="2" seed="5" result="bands"/>
      <feDisplacementMap in="SourceGraphic" in2="bands" scale="13" xChannelSelector="R" yChannelSelector="G" result="shape"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.032 0.16" numOctaves="2" seed="21" result="dabNoise"/>
      <feColorMatrix in="dabNoise" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 1 0 0 0" result="hueField"/>
      <feColorMatrix in="dabNoise" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1 0 0 0 0" result="valueField"/>
      <feComponentTransfer in="hueField" result="coolMask"><feFuncA type="discrete" tableValues="0 0 0 0 0 1 1 1 1 1"/></feComponentTransfer>
      <feComponentTransfer in="hueField" result="warmMask"><feFuncA type="discrete" tableValues="1 1 1 1 0 0 0 0 0 0"/></feComponentTransfer>
      <feComponentTransfer in="valueField" result="lightMask"><feFuncA type="discrete" tableValues="0 0 0 0 0 0 1 1 1 1"/></feComponentTransfer>
      <feComponentTransfer in="valueField" result="darkMask"><feFuncA type="discrete" tableValues="1 1 1 1 0 0 0 0 0 0"/></feComponentTransfer>
      <feColorMatrix in="shape" type="hueRotate" values="-13" result="coolHue"/>
      <feComposite in="coolHue" in2="coolMask" operator="in" result="cool"/>
      <feColorMatrix in="shape" type="hueRotate" values="10" result="warmHue"/>
      <feComposite in="warmHue" in2="warmMask" operator="in" result="warm"/>
      <feFlood flood-color="#ffffff" flood-opacity="0.3"/>
      <feComposite in2="lightMask" operator="in" result="lighter"/>
      <feFlood flood-color="#0c0f24" flood-opacity="0.26"/>
      <feComposite in2="darkMask" operator="in" result="darker"/>
      <feMerge result="mixed">
        <feMergeNode in="shape"/><feMergeNode in="cool"/><feMergeNode in="warm"/><feMergeNode in="lighter"/><feMergeNode in="darker"/>
      </feMerge>
      <feComposite in="mixed" in2="shape" operator="in" result="painted"/>
      <!-- Relief: every dab is its own plateau of paint, with bristle grooves
           along the stroke and a thick rim where the paint ends. -->
      <feTurbulence type="fractalNoise" baseFrequency="0.04 0.5" numOctaves="2" seed="11" result="bristle"/>
      <feComposite in="coolMask" in2="lightMask" operator="arithmetic" k2="0.35" k3="0.4" result="h1"/>
      <feComposite in="h1" in2="warmMask" operator="arithmetic" k2="1" k3="0.2" result="h2"/>
      <feComposite in="h2" in2="darkMask" operator="arithmetic" k2="1" k3="-0.15" result="h3"/>
      <feComposite in="h3" in2="bristle" operator="arithmetic" k2="1" k3="0.24" k4="-0.08" result="h4"/>
      <feComposite in="h4" in2="shape" operator="arithmetic" k1="0.6" k3="0.4" result="heightRaw"/>
      <feGaussianBlur in="heightRaw" stdDeviation="0.5" result="height"/>
      <feDiffuseLighting in="height" surfaceScale="3" diffuseConstant="1" lighting-color="#ffffff" result="diffuse">
        <feDistantLight azimuth="235" elevation="52"/>
      </feDiffuseLighting>
      <feSpecularLighting in="height" surfaceScale="3" specularConstant="0.38" specularExponent="26" lighting-color="#ffffff" result="spec">
        <feDistantLight azimuth="235" elevation="52"/>
      </feSpecularLighting>
      <feComposite in="painted" in2="diffuse" operator="arithmetic" k1="0.95" k2="0.24" result="lit"/>
      <feComposite in="spec" in2="shape" operator="in" result="gloss"/>
      <feComposite in="lit" in2="gloss" operator="arithmetic" k2="1" k3="0.5" result="paint"/>
      <feComposite in="paint" in2="shape" operator="in" result="clipped"/>
      <feDropShadow in="clipped" dx="0.6" dy="1.4" stdDeviation="0.9" flood-color="#000" flood-opacity="0.32"/>
    </filter>
    <!-- The same, gentler, for large panels (cards, inputs, nav, modal) -->
    <filter id="am-acrylic-panel" x="-8%" y="-20%" width="116%" height="145%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.016 0.13" numOctaves="2" seed="5" result="bands"/>
      <feDisplacementMap in="SourceGraphic" in2="bands" scale="9" xChannelSelector="R" yChannelSelector="G" result="shape"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.032 0.16" numOctaves="2" seed="21" result="dabNoise"/>
      <feColorMatrix in="dabNoise" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 1 0 0 0" result="hueField"/>
      <feColorMatrix in="dabNoise" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1 0 0 0 0" result="valueField"/>
      <feComponentTransfer in="hueField" result="coolMask"><feFuncA type="discrete" tableValues="0 0 0 0 0 1 1 1 1 1"/></feComponentTransfer>
      <feComponentTransfer in="hueField" result="warmMask"><feFuncA type="discrete" tableValues="1 1 1 1 0 0 0 0 0 0"/></feComponentTransfer>
      <feComponentTransfer in="valueField" result="lightMask"><feFuncA type="discrete" tableValues="0 0 0 0 0 0 1 1 1 1"/></feComponentTransfer>
      <feComponentTransfer in="valueField" result="darkMask"><feFuncA type="discrete" tableValues="1 1 1 1 0 0 0 0 0 0"/></feComponentTransfer>
      <feColorMatrix in="shape" type="hueRotate" values="-13" result="coolHue"/>
      <feComposite in="coolHue" in2="coolMask" operator="in" result="cool"/>
      <feColorMatrix in="shape" type="hueRotate" values="10" result="warmHue"/>
      <feComposite in="warmHue" in2="warmMask" operator="in" result="warm"/>
      <feFlood flood-color="#ffffff" flood-opacity="0.07"/>
      <feComposite in2="lightMask" operator="in" result="lighter"/>
      <feFlood flood-color="#0c0f24" flood-opacity="0.07"/>
      <feComposite in2="darkMask" operator="in" result="darker"/>
      <feMerge result="mixed">
        <feMergeNode in="shape"/><feMergeNode in="cool"/><feMergeNode in="warm"/><feMergeNode in="lighter"/><feMergeNode in="darker"/>
      </feMerge>
      <feComposite in="mixed" in2="shape" operator="in" result="painted"/>
      <!-- Relief: every dab is its own plateau of paint, with bristle grooves
           along the stroke and a thick rim where the paint ends. -->
      <feTurbulence type="fractalNoise" baseFrequency="0.04 0.5" numOctaves="2" seed="11" result="bristle"/>
      <feComposite in="coolMask" in2="lightMask" operator="arithmetic" k2="0.35" k3="0.4" result="h1"/>
      <feComposite in="h1" in2="warmMask" operator="arithmetic" k2="1" k3="0.2" result="h2"/>
      <feComposite in="h2" in2="darkMask" operator="arithmetic" k2="1" k3="-0.15" result="h3"/>
      <feComposite in="h3" in2="bristle" operator="arithmetic" k2="1" k3="0.24" k4="-0.08" result="h4"/>
      <feComposite in="h4" in2="shape" operator="arithmetic" k1="0.6" k3="0.4" result="heightRaw"/>
      <feGaussianBlur in="heightRaw" stdDeviation="0.5" result="height"/>
      <feDiffuseLighting in="height" surfaceScale="0.8" diffuseConstant="1" lighting-color="#ffffff" result="diffuse">
        <feDistantLight azimuth="235" elevation="52"/>
      </feDiffuseLighting>
      <feSpecularLighting in="height" surfaceScale="0.8" specularConstant="0.3" specularExponent="26" lighting-color="#ffffff" result="spec">
        <feDistantLight azimuth="235" elevation="52"/>
      </feSpecularLighting>
      <feComposite in="painted" in2="diffuse" operator="arithmetic" k1="0.95" k2="0.24" result="lit"/>
      <feComposite in="spec" in2="shape" operator="in" result="gloss"/>
      <feComposite in="lit" in2="gloss" operator="arithmetic" k2="1" k3="0.5" result="paint"/>
      <feComposite in="paint" in2="shape" operator="in" result="clipped"/>
      <feDropShadow in="clipped" dx="0.6" dy="1.4" stdDeviation="0.9" flood-color="#000" flood-opacity="0.22"/>
    </filter>
    <!-- ...and with bigger dabs for splashes -->
    <filter id="am-acrylic-splash" x="-8%" y="-20%" width="116%" height="145%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.01 0.07" numOctaves="2" seed="5" result="bands"/>
      <feDisplacementMap in="SourceGraphic" in2="bands" scale="20" xChannelSelector="R" yChannelSelector="G" result="shape"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.016 0.075" numOctaves="2" seed="21" result="dabNoise"/>
      <feColorMatrix in="dabNoise" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 1 0 0 0" result="hueField"/>
      <feColorMatrix in="dabNoise" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1 0 0 0 0" result="valueField"/>
      <feComponentTransfer in="hueField" result="coolMask"><feFuncA type="discrete" tableValues="0 0 0 0 0 1 1 1 1 1"/></feComponentTransfer>
      <feComponentTransfer in="hueField" result="warmMask"><feFuncA type="discrete" tableValues="1 1 1 1 0 0 0 0 0 0"/></feComponentTransfer>
      <feComponentTransfer in="valueField" result="lightMask"><feFuncA type="discrete" tableValues="0 0 0 0 0 0 1 1 1 1"/></feComponentTransfer>
      <feComponentTransfer in="valueField" result="darkMask"><feFuncA type="discrete" tableValues="1 1 1 1 0 0 0 0 0 0"/></feComponentTransfer>
      <feColorMatrix in="shape" type="hueRotate" values="-13" result="coolHue"/>
      <feComposite in="coolHue" in2="coolMask" operator="in" result="cool"/>
      <feColorMatrix in="shape" type="hueRotate" values="10" result="warmHue"/>
      <feComposite in="warmHue" in2="warmMask" operator="in" result="warm"/>
      <feFlood flood-color="#ffffff" flood-opacity="0.3"/>
      <feComposite in2="lightMask" operator="in" result="lighter"/>
      <feFlood flood-color="#0c0f24" flood-opacity="0.26"/>
      <feComposite in2="darkMask" operator="in" result="darker"/>
      <feMerge result="mixed">
        <feMergeNode in="shape"/><feMergeNode in="cool"/><feMergeNode in="warm"/><feMergeNode in="lighter"/><feMergeNode in="darker"/>
      </feMerge>
      <feComposite in="mixed" in2="shape" operator="in" result="painted"/>
      <!-- Relief: every dab is its own plateau of paint, with bristle grooves
           along the stroke and a thick rim where the paint ends. -->
      <feTurbulence type="fractalNoise" baseFrequency="0.025 0.3" numOctaves="2" seed="11" result="bristle"/>
      <feComposite in="coolMask" in2="lightMask" operator="arithmetic" k2="0.35" k3="0.4" result="h1"/>
      <feComposite in="h1" in2="warmMask" operator="arithmetic" k2="1" k3="0.2" result="h2"/>
      <feComposite in="h2" in2="darkMask" operator="arithmetic" k2="1" k3="-0.15" result="h3"/>
      <feComposite in="h3" in2="bristle" operator="arithmetic" k2="1" k3="0.24" k4="-0.08" result="h4"/>
      <feComposite in="h4" in2="shape" operator="arithmetic" k1="0.6" k3="0.4" result="heightRaw"/>
      <feGaussianBlur in="heightRaw" stdDeviation="0.5" result="height"/>
      <feDiffuseLighting in="height" surfaceScale="3" diffuseConstant="1" lighting-color="#ffffff" result="diffuse">
        <feDistantLight azimuth="235" elevation="52"/>
      </feDiffuseLighting>
      <feSpecularLighting in="height" surfaceScale="3" specularConstant="0.38" specularExponent="26" lighting-color="#ffffff" result="spec">
        <feDistantLight azimuth="235" elevation="52"/>
      </feSpecularLighting>
      <feComposite in="painted" in2="diffuse" operator="arithmetic" k1="0.95" k2="0.24" result="lit"/>
      <feComposite in="spec" in2="shape" operator="in" result="gloss"/>
      <feComposite in="lit" in2="gloss" operator="arithmetic" k2="1" k3="0.5" result="paint"/>
      <feComposite in="paint" in2="shape" operator="in" result="clipped"/>
      <feDropShadow in="clipped" dx="0.6" dy="1.4" stdDeviation="0.9" flood-color="#000" flood-opacity="0.32"/>
    </filter>
    <filter id="am-acrylic-stroke" x="-6%" y="-200%" width="112%" height="500%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.03 0.3" numOctaves="2" seed="6" result="noise"/>
      <feDisplacementMap in="SourceGraphic" in2="noise" scale="5" xChannelSelector="R" yChannelSelector="G" result="shape"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.01 0.6" numOctaves="2" seed="12" result="bristle"/>
      <feComposite in="bristle" in2="shape" operator="in" result="height"/>
      <feDiffuseLighting in="height" surfaceScale="2.5" lighting-color="#ffffff" result="diffuse">
        <feDistantLight azimuth="235" elevation="55"/>
      </feDiffuseLighting>
      <feComposite in="shape" in2="diffuse" operator="arithmetic" k1="0.85" k2="0.32" result="lit"/>
      <feComposite in="lit" in2="shape" operator="in"/>
    </filter>

    <!-- Acrylic, impressionist style: flat matte planes laid in broad
         strokes (band noise drags the plane edges into stroke ends), a warm
         terracotta ground showing at the edges and in thin gaps between
         strokes, dry-brush breakup at the rim and matte canvas tooth. -->
    <filter id="am-acrylic-impressionist" x="-8%" y="-25%" width="116%" height="150%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.012 0.07" numOctaves="2" seed="7" result="strokes"/>
      <feDisplacementMap in="SourceGraphic" in2="strokes" scale="16" xChannelSelector="R" yChannelSelector="G" result="paint"/>
      <!-- warm terracotta underpainting, torn a little wider than the paint -->
      <feMorphology in="SourceAlpha" operator="dilate" radius="2.5" result="grown"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.02 0.08" numOctaves="2" seed="3" result="groundNoise"/>
      <feDisplacementMap in="grown" in2="groundNoise" scale="12" xChannelSelector="R" yChannelSelector="G" result="groundShape"/>
      <feFlood flood-color="#c2633a"/>
      <feComposite in2="groundShape" operator="in" result="ground"/>
      <!-- thin gaps between broad strokes, where the ground shows -->
      <feTurbulence type="fractalNoise" baseFrequency="0.004 0.035" numOctaves="1" seed="19" result="gapNoise"/>
      <feColorMatrix in="gapNoise" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1 0 0 0 0" result="bandField"/>
      <feComponentTransfer in="bandField" result="gaps"><feFuncA type="discrete" tableValues="1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1"/></feComponentTransfer>
      <feComposite in="paint" in2="gaps" operator="in" result="gapped"/>
      <!-- dry-brush breakup where strokes end: bristle noise eats the rim -->
      <feMorphology in="gapped" operator="erode" radius="2.2" result="core"/>
      <feComposite in="gapped" in2="core" operator="out" result="rim"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.05 0.9" numOctaves="1" seed="11" result="bristle"/>
      <feComponentTransfer in="bristle" result="dry"><feFuncA type="discrete" tableValues="0 0 0 0 1 1 1 1 1 1"/></feComponentTransfer>
      <feComposite in="rim" in2="dry" operator="in" result="dryRim"/>
      <feMerge result="brushed"><feMergeNode in="core"/><feMergeNode in="dryRim"/></feMerge>
      <!-- matte canvas tooth -->
      <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="1" seed="5" result="tooth"/>
      <feComposite in="brushed" in2="tooth" operator="arithmetic" k1="0.14" k2="0.93" result="matte"/>
      <feComposite in="matte" in2="brushed" operator="in" result="painted"/>
      <feMerge><feMergeNode in="ground"/><feMergeNode in="painted"/></feMerge>
    </filter>
    <filter id="am-acrylic-impressionist-panel" x="-4%" y="-8%" width="108%" height="116%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.006 0.035" numOctaves="2" seed="7" result="strokes"/>
      <feDisplacementMap in="SourceGraphic" in2="strokes" scale="18" xChannelSelector="R" yChannelSelector="G" result="paint"/>
      <!-- warm terracotta underpainting, torn a little wider than the paint -->
      <feMorphology in="SourceAlpha" operator="dilate" radius="2" result="grown"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.012 0.05" numOctaves="2" seed="3" result="groundNoise"/>
      <feDisplacementMap in="grown" in2="groundNoise" scale="14" xChannelSelector="R" yChannelSelector="G" result="groundShape"/>
      <feFlood flood-color="#c2633a"/>
      <feComposite in2="groundShape" operator="in" result="ground"/>
      <!-- thin gaps between broad strokes, where the ground shows -->
      <feTurbulence type="fractalNoise" baseFrequency="0.004 0.03" numOctaves="1" seed="19" result="gapNoise"/>
      <feColorMatrix in="gapNoise" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1 0 0 0 0" result="bandField"/>
      <feComponentTransfer in="bandField" result="gaps"><feFuncA type="discrete" tableValues="1"/></feComponentTransfer>
      <feComposite in="paint" in2="gaps" operator="in" result="gapped"/>
      <!-- dry-brush breakup where strokes end: bristle noise eats the rim -->
      <feMorphology in="gapped" operator="erode" radius="2.5" result="core"/>
      <feComposite in="gapped" in2="core" operator="out" result="rim"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.05 0.9" numOctaves="1" seed="11" result="bristle"/>
      <feComponentTransfer in="bristle" result="dry"><feFuncA type="discrete" tableValues="0 0 0 0 1 1 1 1 1 1"/></feComponentTransfer>
      <feComposite in="rim" in2="dry" operator="in" result="dryRim"/>
      <feMerge result="brushed"><feMergeNode in="core"/><feMergeNode in="dryRim"/></feMerge>
      <!-- matte canvas tooth -->
      <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="1" seed="5" result="tooth"/>
      <feComposite in="brushed" in2="tooth" operator="arithmetic" k1="0.14" k2="0.93" result="matte"/>
      <feComposite in="matte" in2="brushed" operator="in" result="painted"/>
      <feMerge><feMergeNode in="ground"/><feMergeNode in="painted"/></feMerge>
    </filter>
    <filter id="am-acrylic-impressionist-splash" x="-8%" y="-8%" width="116%" height="116%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.014 0.1" numOctaves="2" seed="7" result="strokes"/>
      <feDisplacementMap in="SourceGraphic" in2="strokes" scale="18" xChannelSelector="R" yChannelSelector="G" result="paint"/>
      <!-- warm terracotta underpainting, torn a little wider than the paint -->
      <feMorphology in="SourceAlpha" operator="dilate" radius="3" result="grown"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.016 0.06" numOctaves="2" seed="3" result="groundNoise"/>
      <feDisplacementMap in="grown" in2="groundNoise" scale="16" xChannelSelector="R" yChannelSelector="G" result="groundShape"/>
      <feFlood flood-color="#c2633a"/>
      <feComposite in2="groundShape" operator="in" result="ground"/>
      <!-- thin gaps between broad strokes, where the ground shows -->
      <feTurbulence type="fractalNoise" baseFrequency="0.004 0.03" numOctaves="1" seed="19" result="gapNoise"/>
      <feColorMatrix in="gapNoise" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1 0 0 0 0" result="bandField"/>
      <feComponentTransfer in="bandField" result="gaps"><feFuncA type="discrete" tableValues="1"/></feComponentTransfer>
      <feComposite in="paint" in2="gaps" operator="in" result="gapped"/>
      <!-- dry-brush breakup where strokes end: bristle noise eats the rim -->
      <feMorphology in="gapped" operator="erode" radius="3" result="core"/>
      <feComposite in="gapped" in2="core" operator="out" result="rim"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.05 0.9" numOctaves="1" seed="11" result="bristle"/>
      <feComponentTransfer in="bristle" result="dry"><feFuncA type="discrete" tableValues="0 0 0 0 1 1 1 1 1 1"/></feComponentTransfer>
      <feComposite in="rim" in2="dry" operator="in" result="dryRim"/>
      <feMerge result="brushed"><feMergeNode in="core"/><feMergeNode in="dryRim"/></feMerge>
      <!-- matte canvas tooth -->
      <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="1" seed="5" result="tooth"/>
      <feComposite in="brushed" in2="tooth" operator="arithmetic" k1="0.14" k2="0.93" result="matte"/>
      <feComposite in="matte" in2="brushed" operator="in" result="painted"/>
      <feMerge><feMergeNode in="ground"/><feMergeNode in="painted"/></feMerge>
    </filter>
    <filter id="am-acrylic-impressionist-stroke" x="-4%" y="-200%" width="108%" height="500%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.01 0.2" numOctaves="2" seed="7" result="strokes"/>
      <feDisplacementMap in="SourceGraphic" in2="strokes" scale="6" xChannelSelector="R" yChannelSelector="G" result="paint"/>
      <!-- warm terracotta underpainting, torn a little wider than the paint -->
      <feMorphology in="SourceAlpha" operator="dilate" radius="1.5" result="grown"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.02 0.2" numOctaves="2" seed="3" result="groundNoise"/>
      <feDisplacementMap in="grown" in2="groundNoise" scale="5" xChannelSelector="R" yChannelSelector="G" result="groundShape"/>
      <feFlood flood-color="#c2633a"/>
      <feComposite in2="groundShape" operator="in" result="ground"/>
      <!-- thin gaps between broad strokes, where the ground shows -->
      <feTurbulence type="fractalNoise" baseFrequency="0.004 0.03" numOctaves="1" seed="19" result="gapNoise"/>
      <feColorMatrix in="gapNoise" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1 0 0 0 0" result="bandField"/>
      <feComponentTransfer in="bandField" result="gaps"><feFuncA type="discrete" tableValues="1"/></feComponentTransfer>
      <feComposite in="paint" in2="gaps" operator="in" result="gapped"/>
      <!-- dry-brush breakup where strokes end: bristle noise eats the rim -->
      <feMorphology in="gapped" operator="erode" radius="1" result="core"/>
      <feComposite in="gapped" in2="core" operator="out" result="rim"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.05 0.9" numOctaves="1" seed="11" result="bristle"/>
      <feComponentTransfer in="bristle" result="dry"><feFuncA type="discrete" tableValues="0 0 0 0 1 1 1 1 1 1"/></feComponentTransfer>
      <feComposite in="rim" in2="dry" operator="in" result="dryRim"/>
      <feMerge result="brushed"><feMergeNode in="core"/><feMergeNode in="dryRim"/></feMerge>
      <!-- matte canvas tooth -->
      <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="1" seed="5" result="tooth"/>
      <feComposite in="brushed" in2="tooth" operator="arithmetic" k1="0.14" k2="0.93" result="matte"/>
      <feComposite in="matte" in2="brushed" operator="in" result="painted"/>
      <feMerge><feMergeNode in="ground"/><feMergeNode in="painted"/></feMerge>
    </filter>
    <!-- Acrylic, realism style: smooth blended paint. Soft edges, a faint
         varnish sheen from a lit dome of the shape, very fine canvas grain
         and a soft warm cast shadow. The modelling gradient is CSS. -->
    <filter id="am-acrylic-realism" x="-12%" y="-30%" width="124%" height="180%" color-interpolation-filters="sRGB">
      <feGaussianBlur in="SourceAlpha" stdDeviation="0.7" result="softA"/>
      <feComposite in="SourceGraphic" in2="softA" operator="in" result="soft"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.95" numOctaves="1" seed="4" result="weave"/>
      <feComposite in="soft" in2="weave" operator="arithmetic" k1="0.08" k2="0.960" result="grainy"/>
      <feComposite in="grainy" in2="soft" operator="in" result="grained"/>
      <feDropShadow in="grained" dx="1" dy="3" stdDeviation="3" flood-color="#2a1a0e" flood-opacity="0.3" result="shadowed"/>
      <feGaussianBlur in="SourceAlpha" stdDeviation="5" result="dome"/>
      <feSpecularLighting in="dome" surfaceScale="4" specularConstant="0.45" specularExponent="20" lighting-color="#fff4e2" result="spec">
        <feDistantLight azimuth="225" elevation="42"/>
      </feSpecularLighting>
      <feComposite in="spec" in2="soft" operator="in" result="sheen"/>
      <feMerge><feMergeNode in="shadowed"/><feMergeNode in="sheen"/></feMerge>
    </filter>
    <filter id="am-acrylic-realism-panel" x="-6%" y="-10%" width="112%" height="125%" color-interpolation-filters="sRGB">
      <feGaussianBlur in="SourceAlpha" stdDeviation="0.6" result="softA"/>
      <feComposite in="SourceGraphic" in2="softA" operator="in" result="soft"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.95" numOctaves="1" seed="4" result="weave"/>
      <feComposite in="soft" in2="weave" operator="arithmetic" k1="0.06" k2="0.970" result="grainy"/>
      <feComposite in="grainy" in2="soft" operator="in" result="grained"/>
      <feDropShadow in="grained" dx="0" dy="4" stdDeviation="8" flood-color="#2a1a0e" flood-opacity="0.22" result="shadowed"/>
      <feMerge><feMergeNode in="shadowed"/></feMerge>
    </filter>
    <filter id="am-acrylic-realism-splash" x="-40%" y="-40%" width="180%" height="200%" color-interpolation-filters="sRGB">
      <feGaussianBlur in="SourceAlpha" stdDeviation="1" result="softA"/>
      <feComposite in="SourceGraphic" in2="softA" operator="in" result="soft"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.95" numOctaves="1" seed="4" result="weave"/>
      <feComposite in="soft" in2="weave" operator="arithmetic" k1="0.08" k2="0.960" result="grainy"/>
      <feComposite in="grainy" in2="soft" operator="in" result="grained"/>
      <feDropShadow in="grained" dx="3" dy="8" stdDeviation="7" flood-color="#2a1a0e" flood-opacity="0.32" result="shadowed"/>
      <feGaussianBlur in="SourceAlpha" stdDeviation="10" result="dome"/>
      <feSpecularLighting in="dome" surfaceScale="4" specularConstant="0.55" specularExponent="20" lighting-color="#fff4e2" result="spec">
        <feDistantLight azimuth="225" elevation="42"/>
      </feSpecularLighting>
      <feComposite in="spec" in2="soft" operator="in" result="sheen"/>
      <feMerge><feMergeNode in="shadowed"/><feMergeNode in="sheen"/></feMerge>
    </filter>
    <filter id="am-acrylic-realism-stroke" x="-4%" y="-200%" width="108%" height="500%" color-interpolation-filters="sRGB">
      <feGaussianBlur in="SourceAlpha" stdDeviation="0.8" result="softA"/>
      <feComposite in="SourceGraphic" in2="softA" operator="in" result="soft"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.95" numOctaves="1" seed="4" result="weave"/>
      <feComposite in="soft" in2="weave" operator="arithmetic" k1="0.04" k2="0.980" result="grainy"/>
      <feComposite in="grainy" in2="soft" operator="in" result="grained"/>
      <feMerge result="shadowed"><feMergeNode in="grained"/></feMerge>
      <feGaussianBlur in="SourceAlpha" stdDeviation="1.5" result="dome"/>
      <feSpecularLighting in="dome" surfaceScale="4" specularConstant="0.4" specularExponent="20" lighting-color="#fff4e2" result="spec">
        <feDistantLight azimuth="225" elevation="42"/>
      </feSpecularLighting>
      <feComposite in="spec" in2="soft" operator="in" result="sheen"/>
      <feMerge><feMergeNode in="shadowed"/><feMergeNode in="sheen"/></feMerge>
    </filter>


    <!-- Charcoal: wobbly hand-drawn line, gritty broken coverage -->
    <filter id="am-charcoal" x="-10%" y="-10%" width="120%" height="120%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.03" numOctaves="3" seed="2" result="wobble"/>
      <feDisplacementMap in="SourceGraphic" in2="wobble" scale="4" xChannelSelector="R" yChannelSelector="G" result="wobbly"/>
      <feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="1" seed="9" result="grit"/>
      <feColorMatrix in="grit" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  1.5 0 0 0 -0.05" result="gritAlpha"/>
      <feComposite in="wobbly" in2="gritAlpha" operator="in"/>
    </filter>


    <!-- Paper: torn construction paper. The colored layer tears a little
         inside a lighter, fibrous core (derived from the paper's own color,
         so it works on light and dark stock), with grain and a soft shadow
         where the piece sits on the sheet below. -->
    <filter id="am-paper" x="-8%" y="-15%" width="116%" height="140%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="4" seed="8" result="tear"/>
      <feMorphology in="SourceGraphic" operator="dilate" radius="1.6" result="grown"/>
      <feDisplacementMap in="grown" in2="tear" scale="9" xChannelSelector="R" yChannelSelector="G" result="coreTorn"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="1" seed="12" result="fiber"/>
      <feDisplacementMap in="coreTorn" in2="fiber" scale="3.5" xChannelSelector="R" yChannelSelector="G" result="coreFuzzy"/>
      <feColorMatrix in="coreFuzzy" type="matrix" values="0.28 0 0 0 0.69  0 0.28 0 0 0.68  0 0 0.28 0 0.65  0 0 0 1 0" result="core"/>
      <feDisplacementMap in="SourceGraphic" in2="tear" scale="7" xChannelSelector="R" yChannelSelector="G" result="color"/>
      <feTurbulence type="fractalNoise" baseFrequency="0.6" numOctaves="2" seed="3" result="grain"/>
      <feDiffuseLighting in="grain" surfaceScale="0.9" lighting-color="#ffffff" result="grainLight">
        <feDistantLight azimuth="225" elevation="60"/>
      </feDiffuseLighting>
      <feComposite in="color" in2="grainLight" operator="arithmetic" k1="0.32" k2="0.73" result="grained"/>
      <feComposite in="grained" in2="color" operator="in" result="piece"/>
      <feGaussianBlur in="coreFuzzy" stdDeviation="2.2" result="blur"/>
      <feOffset in="blur" dx="1" dy="2.5" result="offset"/>
      <feColorMatrix in="offset" type="matrix" values="0 0 0 0 0.08  0 0 0 0 0.06  0 0 0 0 0.04  0 0 0 0.38 0" result="shadow"/>
      <feMerge><feMergeNode in="shadow"/><feMergeNode in="core"/><feMergeNode in="piece"/></feMerge>
    </filter>
    <filter id="am-paper-stroke" x="-5%" y="-150%" width="110%" height="400%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.06" numOctaves="3" seed="9" result="tear"/>
      <feMorphology in="SourceGraphic" operator="dilate" radius="1" result="grown"/>
      <feDisplacementMap in="grown" in2="tear" scale="4" xChannelSelector="R" yChannelSelector="G" result="coreTorn"/>
      <feColorMatrix in="coreTorn" type="matrix" values="0.28 0 0 0 0.69  0 0.28 0 0 0.68  0 0 0.28 0 0.65  0 0 0 1 0" result="core"/>
      <feDisplacementMap in="SourceGraphic" in2="tear" scale="3" xChannelSelector="R" yChannelSelector="G" result="piece"/>
      <feGaussianBlur in="coreTorn" stdDeviation="1" result="blur"/>
      <feOffset in="blur" dx="0.5" dy="1.2" result="offset"/>
      <feColorMatrix in="offset" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 0.3 0" result="shadow"/>
      <feMerge><feMergeNode in="shadow"/><feMergeNode in="core"/><feMergeNode in="piece"/></feMerge>
    </filter>

    <!-- Marker: the stroke shapes, overlap darkening and felt-tip edges live
         in the scribble masks (art-medium.css). This adds faint lighter
         streaks to the ink along the stroke direction. -->
    <filter id="am-marker" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.006 0.3" numOctaves="1" seed="14" result="streak"/>
      <feColorMatrix in="streak" type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 0.5 -0.18" result="sheen"/>
      <feComposite in="sheen" in2="SourceGraphic" operator="in" result="sheenIn"/>
      <feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="sheenIn"/></feMerge>
    </filter>
    <!-- Splashes are masked on ::before and filtered on the element, so
         here ink can pool: overlaps get deeper, not just more opaque. -->
    <filter id="am-marker-splash" x="0" y="0" width="100%" height="100%" color-interpolation-filters="sRGB">
      <feColorMatrix in="SourceGraphic" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" result="a"/>
      <feComponentTransfer in="a" result="deep"><feFuncA type="linear" slope="2.4" intercept="-1.25"/></feComponentTransfer>
      <feColorMatrix in="SourceGraphic" type="matrix" values="0.68 0 0 0 0  0 0.68 0 0 0  0 0 0.72 0 0  0 0 0 0.45 0" result="darker"/>
      <feComposite in="darker" in2="deep" operator="in" result="shade"/>
      <feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="shade"/></feMerge>
    </filter>

  </defs>
</svg>`;

/** Inject the SVG filter definitions once. Safe to call repeatedly. */
export function installFilters(doc = globalThis.document) {
  if (!doc || doc.getElementById('am-filters')) return;
  const tpl = doc.createElement('template');
  tpl.innerHTML = FILTERS.trim();
  doc.body.prepend(tpl.content.firstElementChild);
}

/** Switch the medium for an element and everything inside it. */
export function setMedium(el, medium) {
  if (!MEDIUMS.includes(medium)) throw new Error(`Unknown medium "${medium}". Use one of: ${MEDIUMS.join(', ')}`);
  el.setAttribute('data-medium', medium);
}

/** Switch the style (acrylic: impasto | impressionist | realism, charcoal:
 *  newsprint | sketchbook | kraft, marker: plain | notebook | parchment) for an
 *  element and everything inside it. Each medium ignores other mediums' styles. */
export function setStyle(el, style) {
  if (!STYLES.includes(style)) throw new Error(`Unknown style "${style}". Use one of: ${STYLES.join(', ')}`);
  el.setAttribute('data-style', style);
}

/** Switch light/dark for an element and everything inside it. "auto" follows the OS. */
export function setTheme(el, theme) {
  if (!THEMES.includes(theme)) throw new Error(`Unknown theme "${theme}". Use one of: ${THEMES.join(', ')}`);
  el.setAttribute('data-theme', theme);
}

if (typeof document !== 'undefined') {
  if (document.body) installFilters();
  else document.addEventListener('DOMContentLoaded', () => installFilters(), { once: true });
}
