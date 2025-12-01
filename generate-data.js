import fs from "fs";
// Define bounding boxes for major, densely populated regions in India
// This ensures generated points land in states, avoiding oceans and neighbors.
const REGIONAL_BOUNDS = [
  // North/Delhi/NCR/Punjab
  { minLat: 27, maxLat: 32, minLng: 75, maxLng: 78, weight: 3 },
  // West/Maharashtra/Gujarat
  { minLat: 18, maxLat: 23, minLng: 72, maxLng: 78, weight: 4 },
  // South/Karnataka/Tamil Nadu/Andhra
  { minLat: 12, maxLat: 18, minLng: 76, maxLng: 80, weight: 3 },
  // East/Kolkata/Bihar
  { minLat: 22, maxLat: 26, minLng: 85, maxLng: 90, weight: 2 },
  // Central/MP/UP
  { minLat: 23, maxLat: 28, minLng: 78, maxLng: 83, weight: 3 },
];

// === FUNCTION: Generate Random Users within Specific Regions ===
function generateRandomUsers(count) {
  const users = [];
  let totalWeight = REGIONAL_BOUNDS.reduce(
    (sum, region) => sum + region.weight,
    0
  );

  for (let i = 0; i < count; i++) {
    // 1. Select a region based on its weight (to simulate density)
    let rand = Math.random() * totalWeight;
    let selectedRegion = null;
    for (const region of REGIONAL_BOUNDS) {
      if (rand < region.weight) {
        selectedRegion = region;
        break;
      }
      rand -= region.weight;
    }

    if (!selectedRegion) continue;

    // 2. Generate random coordinates within the selected region
    const lat =
      Math.random() * (selectedRegion.maxLat - selectedRegion.minLat) +
      selectedRegion.minLat;
    const lng =
      Math.random() * (selectedRegion.maxLng - selectedRegion.minLng) +
      selectedRegion.minLng;

    users.push([lat, lng]);
  }
  return users;
}
const otherUsersLocations = generateRandomUsers(1200000);

fs.writeFileSync("data.js", JSON.stringify(otherUsersLocations));
