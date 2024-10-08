import React, { useState } from 'react';
import axios from 'axios';
import PaperVisualization from '../visualizer';
import { Link } from 'react-router-dom';


// Import MUI components
import { Container, Typography, TextField, Button, Box, Paper, CircularProgress, Grid2, AppBar, Toolbar } from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';

const Home = () => {
    const [pieceWidth, setPieceWidth] = useState('');
    const [pieceHeight, setPieceHeight] = useState('');
    const [submittedWidth, setSubmittedWidth] = useState(null);
    const [submittedHeight, setSubmittedHeight] = useState(null);
    const [result, setResult] = useState(null);
    const [combi, setCombination] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        try {
            const response = await axios.post('http://127.0.0.1:8000/optimizeall', {
                piece_width: pieceWidth,
                piece_height: pieceHeight
            });
            setResult(response.data);
            var combination = {
                num_cols_landscape: response.data.best_combination.num_cols_landscape,
                remaining_width: response.data.best_combination.remaining_width,
                case: response.data.best_combination.case
            };
            if (response.data.best_combination.case === "rows") {
                combination = {
                    num_rows_landscape: response.data.best_combination.num_rows_landscape,
                    remaining_height: response.data.best_combination.remaining_height,
                    case: response.data.best_combination.case
                };
            }
            setCombination(combination);
            setSubmittedWidth(pieceWidth);
            setSubmittedHeight(pieceHeight);
        } catch (error) {
            console.error('Error:', error);
        }
        setLoading(false);
    };

    return (
        <Box sx={{ flexGrow: 1 }}>
            {/* AppBar for Sign In and Register Buttons */}
            <AppBar position="static">
                <Toolbar>
                    <Typography variant="h6" sx={{ flexGrow: 1}}>
                        Dynamic Cutting Optimizer
                    </Typography>
                    <Button component={Link} to="/login" color="inherit">Sign In</Button>
                    <Button component={Link} to="/register" color="inherit">Register</Button>
                </Toolbar>
            </AppBar>

            <Container maxWidth="lg" sx={{ backgroundColor: 'background.default', padding: 4, marginTop: 2 }}>
                <Grid2 container spacing={4} justifyContent="space-between">
                    <Grid2 item xs={12} md={6}>
                        <Paper elevation={3} sx={{ padding: 4 }}>
                            <Typography variant="h4" gutterBottom align="center">
                                Dynamic Cutting Optimizer
                            </Typography>
                            <Box
                                component="form"
                                onSubmit={handleSubmit}
                                sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}
                            >
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
                                <Button
                                    variant="contained"
                                    color="primary"
                                    type="submit"
                                    fullWidth
                                    disabled={loading || !pieceWidth || !pieceHeight}
                                >
                                    {loading ? <CircularProgress size={24} color="inherit" /> : 'Optimize'}
                                </Button>
                            </Box>
                        </Paper>
                    </Grid2>

                    {/* Right Paper with Results */}
                    <Grid2 item xs={12} md={6}>
                        {result ? (
                            <Paper elevation={3} sx={{ padding: 4 }}>
                                <Typography variant="h6">Optimization Results</Typography>
                                <Typography variant="body1">Max Pieces: {result.all_max_pieces}</Typography>
                                <Typography variant="body1">Min Waste: {result.all_min_waste}%</Typography>
                                <Typography variant="body1">Paper Width: {result.paper_width}</Typography>
                                <Typography variant="body1">Paper Height: {result.paper_height}</Typography>
                                <Typography variant="h6">Cutting Layout Visualization</Typography>
                                <Box sx={{ marginTop: 2 }}>
                                    <PaperVisualization
                                        paperWidth={result.paper_width}
                                        paperHeight={result.paper_height}
                                        pieceWidth={submittedWidth}
                                        pieceHeight={submittedHeight}
                                        combination={combi}
                                    />
                                </Box>
                            </Paper>
                        ) : (
                            <Paper elevation={3} sx={{ padding: 4 }}>
                                <Typography variant="h6" align="center">
                                    Please input dimensions and click "Optimize" to see the results.
                                </Typography>
                            </Paper>
                        )}
                    </Grid2>
                </Grid2>
            </Container>
        </Box>
    );
};

export default Home;
