import { Box3, Vector3 } from "three";

/** Fit the selected bounds in the visible inspection area at the chosen view. */
export function inspectionDistance(
  box: Box3,
  viewDirection: Vector3,
  verticalFov: number,
  viewportHeight: number,
  availableWidth: number,
  availableHeight: number,
) {
  const direction = viewDirection.clone().normalize();
  const right = new Vector3().crossVectors(new Vector3(0, 1, 0), direction).normalize();
  const up = new Vector3().crossVectors(direction, right);
  const center = box.getCenter(new Vector3());
  const tangent = Math.tan((verticalFov * Math.PI) / 360);
  const horizontalLimit = (tangent * availableWidth) / viewportHeight;
  const verticalLimit = (tangent * availableHeight) / viewportHeight;
  let distance = 0.07;
  for (const x of [box.min.x, box.max.x]) {
    for (const y of [box.min.y, box.max.y]) {
      for (const z of [box.min.z, box.max.z]) {
        const corner = new Vector3(x, y, z).sub(center);
        // Depth changes perspective; it is not an on-screen width or height.
        const depth = corner.dot(direction);
        distance = Math.max(
          distance,
          depth + 0.01,
          depth + (Math.abs(corner.dot(right)) * 1.2) / horizontalLimit,
          depth + (Math.abs(corner.dot(up)) * 1.2) / verticalLimit,
        );
      }
    }
  }
  return distance;
}
