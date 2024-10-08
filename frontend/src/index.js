import React from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import App from './App';
import theme from './theme/theme'
import { ThemeProvider } from '@emotion/react';

// Grab the root element from your HTML
const container = document.getElementById('root');

// Create a root
const root = createRoot(container);

root.render(
  <ThemeProvider theme={theme}>
    <BrowserRouter>
        <App />
    </BrowserRouter>
  </ThemeProvider>

);
