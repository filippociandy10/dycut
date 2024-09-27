import React, { useState } from 'react';
import axios from 'axios';
import PaperVisualization from './visualizer';

// Import MUI components
import { Container, Typography, TextField, Button, Box, Paper } from '@mui/material';

const App = () => {
    const [pieceWidth, setPieceWidth] = useState('');
    const [pieceHeight, setPieceHeight] = useState('');
    const [result, setResult] = useState(null);
    const [combi, setCombination] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post('http://127.0.0.1:8000/optimizeall', {
                piece_width: pieceWidth,
                piece_height: pieceHeight
            });
            setResult(response.data);  // Update the result state
            const combination = {
                num_rows_landscape: response.data.best_combination.num_rows_landscape,
                remaining_height: response.data.best_combination.remaining_height 
            };
            setCombination(combination)
            console.log(combination)
        } catch (error) {
            console.error('Error:', error);
        }
    };



    return (
        <Container maxWidth="sm">
            <Paper elevation={3} sx={{ padding: 4, marginTop: 4 }}>
                <Typography variant="h4" gutterBottom align="center">
                    Dynamic Cutting Optimizer
                </Typography>
                <Box component="form" onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                    <TextField
                        label="Piece Width"
                        variant="outlined"
                        type="number"
                        value={pieceWidth}
                        onChange={e => setPieceWidth(e.target.value)}
                        required
                        fullWidth
                    />
                    <TextField
                        label="Piece Height"
                        variant="outlined"
                        type="number"
                        value={pieceHeight}
                        onChange={e => setPieceHeight(e.target.value)}
                        required
                        fullWidth
                    />
                    <Button variant="contained" color="primary" type="submit" fullWidth>
                        Optimize
                    </Button>
                </Box>
                {result && (
                    <Box sx={{ marginTop: 4 }}>
                        <Typography variant="h6">Results:</Typography>
                        <Typography>Max Pieces: {result.all_max_pieces}</Typography>
                        <Typography>Min Waste: {result.all_min_waste}</Typography>
                        <Typography>Width: {result.paper_width}</Typography>
                        <Typography>Height: {result.paper_height}</Typography>
                        <div>
                            <h1>Cutting Layout Visualization</h1>
                            <PaperVisualization
                                paperWidth={result.paper_width}
                                paperHeight={result.paper_height}
                                pieceWidth={pieceWidth}
                                pieceHeight={pieceHeight}
                                combination={combi}
                            />
                        </div>
                    </Box>
                )}
            </Paper>
        </Container>
    );
};

export default App;
