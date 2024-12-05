import type { Point } from "$types/point";

export function vectorMin(pointA: Point, pointB: Point) {
    return {
        x: Math.min(pointA.x, pointB.x),
        y: Math.min(pointA.y, pointB.y)
    } 
}

export function vectorMax(pointA: Point, pointB: Point) {
    return {
        x: Math.max(pointA.x, pointB.x),
        y: Math.max(pointA.y, pointB.y)
    } 
}
