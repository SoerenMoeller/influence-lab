import type { DrawRectState, MouseEventHandler } from "./draw-rect.types";
import type { SvgSelection } from "$types/svg";
import * as d3 from "d3";
import type { Point } from "$types/point";
import { vectorMax, vectorMin } from "$modules/vector";

export function init(parentSvg: SvgSelection) {
    const drawRectState: DrawRectState = {
        origin: { x: 0, y: 0 },
        isDrawing: false,
        rectElement: undefined
    };     

    const eventHandlers: MouseEventHandler = {
        mousedown: handleOnMouseDown,
        mousemove: handleOnMouseMove,
        mouseup: handleOnMouseUp,
    };
    
    for (const eventName in eventHandlers) {
        parentSvg.on(eventName, (event: MouseEvent) =>
                     eventHandlers[eventName](event, parentSvg, drawRectState));
    }
}

function handleOnMouseDown(event: MouseEvent, parentSvg: SvgSelection, 
                           drawRectState: DrawRectState) {
    const [x, y] = d3.pointer(event);
    
    drawRectState.isDrawing = true;
    drawRectState.origin = { x, y }
    
    // init rect element
    const rect = parentSvg.append("rect")
        .attr("x", x)
        .attr("y", y)
        .attr("fill-opacity", 0)
        .attr("stroke", "black");
        
    drawRectState.rectElement = rect;
}

function handleOnMouseMove(event: MouseEvent, parentSvg: SvgSelection, 
                           drawRectState: DrawRectState) {
    if (!drawRectState.isDrawing) return;
    if (drawRectState.rectElement === undefined) {
        console.error("Cannot draw Rect-Element, as it is undefined.");
        return;
    }
     
    const [x, y] = d3.pointer(event);

    const startPosition: Point = vectorMin({x, y}, drawRectState.origin);
    const endPosition: Point = vectorMax({x, y}, drawRectState.origin);
    
    drawRectState.rectElement
        .attr("x", startPosition.x)
        .attr("y", startPosition.y)
        .attr("width", endPosition.x - startPosition.x)
        .attr("height", endPosition.y - startPosition.y);
}

function handleOnMouseUp(event: MouseEvent, parentSvg: SvgSelection, 
                         drawRectState: DrawRectState) {
    if (!drawRectState.isDrawing) return;
    drawRectState.isDrawing = false;
}
