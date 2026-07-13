# SurfView 🌊

Find a surf spot on a map and "drop in" to a street-view-style, first-person
simulation of the ocean there — rendered from the **real conditions at that
spot right now**.

## What it does

1. **Spot map** — an interactive world map (Leaflet + OpenStreetMap) seeded
   with 38 world-class surf spots (Pipeline, Teahupo'o, J-Bay, Nazaré, …),
   plus a searchable sidebar. Marker colours encode the break type
   (reef / point / beach / big-wave / river-mouth).
2. **Live conditions** — clicking a spot fetches the current sea state from
   the free [Open-Meteo](https://open-meteo.com/) Marine + Weather APIs
   (no API key): wave height, swell height/period/direction, wind, water
   and air temperature, cloud cover, and a 72-hour wave-height sparkline.
   A simple heuristic calls the session ("Firing", "Clean", "Blown out", …)
   based on swell period, size and whether the wind is offshore for that
   beach's orientation.
3. **Drop in** — a full-screen, first-person WebGL ocean you can drag to
   look around, driven entirely by the live data:
   - swell **amplitude** from the reported height, **wavelength** from the
     period (deep-water dispersion, `L = gT²/2π`, shoaled for realism),
   - swell **direction** relative to the beach's real orientation,
   - **wind chop** scaled by wind speed — and groomed when the wind is
     offshore,
   - **sun position** computed from the spot's latitude/longitude and the
     current UTC time (dawn patrol looks like dawn; a midnight check of
     Uluwatu is dark with stars),
   - **cloud cover** from the live weather.

The wave field is an original sum-of-directional-waves heightfield
raymarched in a single fragment shader (no 3D framework), with fresnel sky
reflection, sun glint, crest foam and aerial perspective.

Each break type also carries a parametric seabed — reef slab with a deep
channel, angled point contours, sandbars with rip gaps, river-mouth wedge,
big-wave ledge — and the swell reacts to it with surf physics: shoaling
amplification, crests pitching forward, breaking where height exceeds
~0.78× depth (the lip lights up and the wave rolls on as whitewater), and
turquoise water over the shallows. The break depth scales with the day's
swell, so bigger days break wider and further out, and sets roll through
on a slow envelope with lulls between them.

## Running it

It's a fully static app — no build step, no keys:

```sh
cd surfview
python3 -m http.server 8000   # or any static file server
# open http://localhost:8000
```

Opening `index.html` directly from disk also works in most browsers.
Leaflet is vendored in `vendor/`; the only network calls are OpenStreetMap
tiles and the Open-Meteo APIs. If the APIs are unreachable, the app falls
back to typical conditions and says so.

## Layout

```
surfview/
├── index.html        app shell
├── css/style.css     UI styling
├── js/spots.js       curated spot database (incl. beach orientation)
├── js/app.js         map, search, live data, solar position, HUD
├── js/ocean.js       WebGL ocean: shader + raymarcher + input
└── vendor/           Leaflet 1.9.4 (BSD-2-Clause)
```

## Ideas for later

- Tide curve (Open-Meteo has no tide data; would need NOAA/Stormglass).
- Shore/reef geometry so waves visibly break and peel like the real spot.
- WebXR mode — look around on a phone or headset.
- Favourites, spot submission, and swell alerts.
