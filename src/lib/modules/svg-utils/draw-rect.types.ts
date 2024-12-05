import type { RectSelection, SvgSelection } from "$types/svg";
import type { Point } from "$types/point";

export type DrawRectState = {
    isDrawing: boolean;
    origin: Point;
    rectElement: RectSelection | undefined;
}

export type MouseEventHandler = 
    Record<string, (event: MouseEvent, svg: SvgSelection, state: DrawRectState) => void>;

