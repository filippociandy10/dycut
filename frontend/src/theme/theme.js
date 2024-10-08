import { createTheme } from '@mui/material/styles';

// Define your custom theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',  // Primary color (adjust to match your design)
    },
    secondary: {
      main: '#dc004e',  // Secondary color (adjust to match your design)
    },
  },
  typography: {
    fontFamily: 'Roboto, Arial, sans-serif',  // Default font family
    h1: {
      fontSize: '2.5rem',
      fontWeight: 600,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 500,
    },
    body1: {
      fontSize: '1rem',
      color: '#333',
    },
  },
  // You can customize spacing, breakpoints, etc., based on your design needs
});

export default theme;
