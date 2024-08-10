import React, { useState } from 'react';
import axios from 'axios';
import { TextField, Button, Grid, Paper, Typography, createTheme, ThemeProvider, Select, MenuItem, FormControl, InputLabel, Box } from '@mui/material';

// Create a custom theme with the desired primary color
const theme = createTheme({
    palette: {
        primary: {
            main: '#6C83FF', // Custom primary color
        },
    },
    typography: {
        fontFamily: 'Pretendard', // Apply the local font to the MUI theme
    },
});

const GenderFreeTranslator = () => {
    const [inputText, setInputText] = useState('');
    const [outputText, setOutputText] = useState([]);
    const [diffIndexes, setDiffIndexes] = useState([]);
    const [originalSentences, setOriginalSentences] = useState([]);
    const [community, setCommunity] = useState('스누라이프'); // Default community selection

    const handleTranslate = async () => {
        try {
            const response = await axios.post('https://5a8e-2001-2d8-6937-8f75-299e-fb06-bf3f-9eae.ngrok-free.app/api/v1/translate', {
                input_text: inputText
            });
            setOutputText(response.data.strings);
            setDiffIndexes(response.data.isdiff);
            setOriginalSentences(inputText.split('.').map(sentence => sentence.trim()).filter(sentence => sentence));
        } catch (error) {
            console.error('Error during translation:', error);
        }
    };

    const handleInputChange = (e) => {
        setInputText(e.target.value);
    };

    const handleCommunityChange = (event) => {
        setCommunity(event.target.value);
    };

    return (
        <ThemeProvider theme={theme}>
            <Box sx={{ padding: '20px' }}>
                <Grid container spacing={2} direction="column" alignItems="center">
                    

                    {/* Community Selection on the right */}
                    <Grid item xs={12} sm={4} container justifyContent="flex-end" alignItems="center" style={{ marginTop: '20px' }}>
                        <FormControl variant="outlined" style={{ minWidth: 120 }}>
                            <InputLabel>Community</InputLabel>
                            <Select
                                value={community}
                                onChange={handleCommunityChange}
                                label="Community"
                            >
                                <MenuItem value="스누라이프">스누라이프</MenuItem>
                                <MenuItem value="오르비">오르비</MenuItem>
                                <MenuItem value="에브리타임">에브리타임</MenuItem>
                            </Select>
                        </FormControl>
                    </Grid>
                    {/* Logo */}
                    <Grid item xs={12} sm={4} container justifyContent="center">
                        <img src={`${process.env.PUBLIC_URL}/assets/logo.png`} alt="Logo" style={{ maxHeight: '100px' }} />
                    </Grid>
                </Grid>

                <Grid container spacing={4} justifyContent="center" style={{ marginTop: '20px' }}>
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
                                sx={{ fontFamily: 'Pretendard' }} // Apply the font specifically to the TextField
                            />
                        </Paper>
                    </Grid>

                    {/* Output Box */}
                    <Grid item xs={12} md={5}>
                        <Paper elevation={3} style={{ padding: '20px', height: '300px' }}>
                            <Typography variant="body1" component="div" style={{ height: '100%', overflowY: 'auto' }}>
                                {outputText.map((sentence, index) => (
                                    <span key={index} style={{ color: diffIndexes.includes(index) ? 'green' : 'black' }}>
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
                        GenErase!!!
                    </Button>
                </Grid>

                {/* Comparison of Original and Translated Sentences */}
                <Grid container justifyContent="center" style={{ marginTop: '20px' }}>
                    <Grid item xs={12} md={10}>
                        <Paper elevation={3} style={{ padding: '20px' }}>
                            {originalSentences.map((sentence, index) => (
                                diffIndexes.includes(index) ? (
                                    <div key={index} style={{ display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
                                        <Typography style={{ color: 'red', marginRight: '10px' }}>
                                            {sentence}
                                        </Typography>
                                        <span style={{ marginRight: '10px' }}>→</span>
                                        <Typography style={{ color: 'green' }}>
                                            {outputText[index]}
                                        </Typography>
                                    </div>
                                ) : null
                            ))}
                        </Paper>
                    </Grid>
                </Grid>
            </Box>
        </ThemeProvider>
    );
};

export default GenderFreeTranslator;
