import React, { useState } from 'react';
import axios from 'axios';
import { TextField, Button, Grid, Paper, Typography } from '@mui/material';

const GenderFreeTranslator = () => {
    const [inputText, setInputText] = useState('');  // State for storing the user's input
    const [outputText, setOutputText] = useState([]);  // State for storing the translated text as an array of sentences
    const [diffIndexes, setDiffIndexes] = useState([]);  // State for storing indexes of modified sentences

    // Function to handle the translation process
    const handleTranslate = async () => {
        try {
            // Sending the input text to the backend API
            const response = await axios.post('http://localhost:8000/translate', {
                text: inputText
            });
            // Storing the response data
            setOutputText(response.data.strings);
            setDiffIndexes(response.data.isdiff);
        } catch (error) {
            console.error('Error during translation:', error);
        }
    };

    // Function to handle changes in the input text area
    const handleInputChange = (e) => {
        setInputText(e.target.value);
    };

    return (
        <div style={{ padding: '50px' }}>
            <Typography variant="h4" gutterBottom align="center">
                GenEraser
            </Typography>
            <Grid container spacing={4} justifyContent="center">
                {/* Input Box */}
                <Grid item xs={12} md={5}>
                    <Paper elevation={3} style={{ padding: '20px', height: '300px' }}>
                        <TextField
                            label="Enter text"
                            multiline
                            rows={10}
                            variant="outlined"
                            fullWidth
                            value={inputText}
                            onChange={handleInputChange}
                            style={{ height: '100%' }}
                        />
                    </Paper>
                </Grid>

                {/* Output Box */}
                <Grid item xs={12} md={5}>
                    <Paper elevation={3} style={{ padding: '20px', height: '300px' }}>
                        <Typography variant="h6">Output:</Typography>
                        <Typography variant="body1" component="div" style={{ height: '100%', overflowY: 'auto' }}>
                            {outputText.map((sentence, index) => (
                                <span key={index} style={{ color: diffIndexes.includes(index) ? 'red' : 'black' }}>
                                    {sentence}.{' '}
                                </span>
                            ))}
                        </Typography>
                    </Paper>
                </Grid>
            </Grid>

            {/* Translate Button */}
            <Grid container justifyContent="center" style={{ marginTop: '20px' }}>
                <Button variant="contained" color="primary" onClick={handleTranslate}>
                    Translate
                </Button>
            </Grid>
        </div>
    );
};

export default GenderFreeTranslator;
