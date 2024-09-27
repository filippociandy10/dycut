import React from 'react';
import { Stage, Layer, Rect } from 'react-konva';
import { Container, Typography, Box } from '@mui/material';

// Function to create the layout of pieces based on combination
const generateLayout = (paperWidth, paperHeight, pieceWidth, pieceHeight, combination) => {
    const layout = [];
    const numRowsLandscape = combination.num_rows_landscape;
    const remainingHeight = combination.remaining_height;

    // Add landscape pieces
    for (let row = 0; row < numRowsLandscape; row++) {
        for (let col = 0; col < Math.floor(paperWidth / pieceWidth); col++) {
            layout.push({
                x: col * pieceWidth,
                y: row * pieceHeight,
                width: pieceWidth,
                height: pieceHeight,
            });
        }
    }

    // Add portrait pieces in the remaining height
    for (let row = 0; row < Math.floor(remainingHeight / pieceWidth); row++) {
        for (let col = 0; col < Math.floor(paperWidth / pieceHeight); col++) {
            layout.push({
                x: col * pieceHeight,
                y: paperHeight - remainingHeight + row * pieceWidth,
                width: pieceHeight,
                height: pieceWidth,
            });
        }
    }

    return layout;
};

// Main component to visualize the optimized layout
const PaperVisualization = ({ paperWidth, paperHeight, pieceWidth, pieceHeight, combination }) => {
    const layout = generateLayout(paperWidth, paperHeight, pieceWidth, pieceHeight, combination);

    // Scaling factor to fit the paper into the canvas
    const canvasWidth = 500;  // Canvas width
    const canvasHeight = 500; // Canvas height

    const scalingFactor = Math.min(canvasWidth / paperWidth, canvasHeight / paperHeight);

    return (
        <Container maxWidth="sm">
            <Box sx={{ marginTop: 4, textAlign: 'center' }}>
                <Typography variant="h6">Cut Visualization</Typography>

                {/* Render the paper and pieces using React Konva */}
                <Stage width={canvasWidth} height={canvasHeight}>
                    <Layer>
                        {/* Draw the paper boundary */}
                        <Rect
                            x={0}
                            y={0}
                            width={paperWidth * scalingFactor}
                            height={paperHeight * scalingFactor}
                            stroke="black"
                            strokeWidth={2}
                            fill="white"
                        />
                        
                        {/* Draw each piece */}
                        {layout.map((piece, index) => (
                            <Rect
                                key={index}
                                x={piece.x * scalingFactor}
                                y={piece.y * scalingFactor}
                                width={piece.width * scalingFactor}
                                height={piece.height * scalingFactor}
                                stroke="red"
                                strokeWidth={1}
                                fill="transparent"
                            />
                        ))}
                    </Layer>
                </Stage>
            </Box>
        </Container>
    );
};

export default PaperVisualization;
