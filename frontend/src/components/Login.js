import React, { useState } from 'react';
import { TextField, Button, Typography, Container, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const navigate = useNavigate();  // For navigation after login

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Make a POST request to the backend for sign-in
      const response = await axios.post('http://127.0.0.1:8000/login', {
        username,
        password,
      });

      // If login is successful, store the token and redirect to dashboard
      localStorage.setItem('auth_token', response.data.token);
      navigate('/');  // Redirect to dashboard or another protected route

    } catch (error) {
      // Handle any error responses from the backend
      if (error.response) {
        setMessage(error.response.data.error);
      }
    }
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
        }}
      >
        <Typography component="h1" variant="h5">
          Sign In
        </Typography>
        <form onSubmit={handleSubmit} style={{ width: '100%', marginTop: '1rem' }}>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            label="Username"
            name="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            label="Password"
            type="password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            color="primary"
            sx={{ mt: 3, mb: 2 }}
          >
            Sign In
          </Button>
          {message && (
            <Typography color="error">
              {message}
            </Typography>
          )}
        </form>
      </Box>
    </Container>
  );
};

export default Login;
