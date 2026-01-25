Here are the updated files to implement the "blind" typing experience with character-by-character highlighting and a hidden input field.

### Summary of Changes:
1.  **`src/js/utils.js`**: Added `getEndIndexInTashkeel` to map the typed letters (without Tashkeel) to the corresponding position in the displayed text (with Tashkeel).
2.  **`src/css/styles.css`**:
    *   Hid the `#inputField` visually (opacity 0, absolute position) but kept it functional for IME/Mobile support.
    *   Added `.correct-char` class to color typed letters green.
    *   Added a blinking cursor effect (`.cursor-active`) to the current word.
3.  **`src/js/logic.js`**:
    *   Updated `handleInput` to perform character-level validation.
    *   Added logic to inject `<span>` tags inside the current word to highlight typed characters while preserving Tashkeel.
    *   Added a global click listener to ensure the hidden input stays focused.
4.  **`index.html`**: Minor cleanup to input attributes.

---

### 1. src/js/utils.js

```javascript
export function convertToArabicNumber(englishNumber) {
    englishNumber = englishNumber.toString()

    const arabicNumbers = ["٠", "١", "٢", "٣", "٤", "٥", "٦", "٧", "٨", "٩"];
    const englishDigits = "0123456789";
    const englishToArabicMap = {};

    for (let i = 0; i < englishDigits.length; i++) {
        englishToArabicMap[englishDigits[i]] = arabicNumbers[i];
    }

    const arabicNumber = englishNumber.replace(/\d/g, (match) => englishToArabicMap[match]);

    return arabicNumber;
}

export function createNoTashkeelString(noTashkeelAyahs) {
    noTashkeelAyahs = noTashkeelAyahs.map((ayah) => removeTashkeel(ayah))

    let processedString = noTashkeelAyahs.join(" ")

    // This handles an issue with \u06D6-\u06DE (the stop signs). They become spaces when removed.
    // This results in 2 consecutive spaces. This is replaced with one space using this code.
    processedString = processedString.replace(/\s{2,}/g, ' ');
    return processedString
}

export function removeTashkeel(text) {
    let noTashkeel = text

    noTashkeel = noTashkeel.replace(/\u0670/g, '\u0627');  // replace the small subscript alef with normal alef
    noTashkeel = noTashkeel.replace(/\u0671/g, '\u0627');  // replace the alef wasl with alef

    // fix an issue with the ya encoding
    // (persian for some reason). Note this replaces all normal ya, but also the ya for alef layena.
    //  so for something like فى it is written في. Not sure if this is fine, check with someone arabic literate
    noTashkeel = noTashkeel.replace(/\u06CC/g, '\u064A');

    // handle hamza above the line extender char. (the part below removes this char, so we have to handle here.)
    noTashkeel = noTashkeel.replace(/\u0640\u0654/g, '\u0626'); // ya


    // this removes everything that isnt a main char, or a hamza above or below, or a spacebar
    // noTashkeel = noTashkeel.replace(/[^\u0621-\u063A\u0641-\u064A\u0654-\u0655 ]/g, '');
    noTashkeel = noTashkeel.replace(/[^\u0621-\u063A\u0641-\u064A\u0654-\u0655 ]/g, '');

    // // change the ya with hamza underneath and to ya with hamza above as this is available on keyboard
    noTashkeel = noTashkeel.replace(/\u0649\u0655/g, '\u0626');

    // fixes a bug with words like: الأيات . the lam then alef then hamza causes an issue.
    noTashkeel = noTashkeel.replace(/\u0654\u0627/g, '\u0623');
    noTashkeel = noTashkeel.replace(/\u0655\u0627/g, '\u0625');

    // for ya and waw with hamza above (Havent checked if they apply). 
    noTashkeel = noTashkeel.replace(/\u0654\u0648/g, '\u0624'); // waw
    noTashkeel = noTashkeel.replace(/\u0654\u064A/g, '\u0626'); // ya

    return noTashkeel
}

/**
 * Calculates the index in the original (Tashkeel) string that corresponds 
 * to the end of the Nth character in the No-Tashkeel string.
 * Used for highlighting logic.
 * 
 * @param {string} textWithTashkeel - The original text.
 * @param {number} noTashkeelLength - Number of "main" characters typed.
 * @returns {number} The slice index for the original string.
 */
export function getEndIndexInTashkeel(textWithTashkeel, noTashkeelLength) {
    if (noTashkeelLength === 0) return 0;
    
    let mainCharCount = 0;
    let i = 0;
    
    // Regex for characters that count as "main" characters (same logic as removeTashkeel roughly)
    // We want to count letters, hamzas, but skip tashkeel marks.
    // Common Arabic letters range: \u0621-\u064A
    const mainCharRegex = /[\u0621-\u063A\u0641-\u064A\u0654-\u0655]/;

    for (i = 0; i < textWithTashkeel.length; i++) {
        const char = textWithTashkeel[i];
        
        // If it's a main character
        if (mainCharRegex.test(char)) {
            mainCharCount++;
        }
        
        // Special handling: Alef Wasl \u0671 and Superscript Alef \u0670 are usually mapped to Alef
        // so they count as 1 main char.
        else if (char === '\u0671' || char === '\u0670') {
            mainCharCount++;
        }
        
        if (mainCharCount === noTashkeelLength) {
            // We found the last main char. 
            // We must continue to include any subsequent tashkeel marks attached to this letter.
            let j = i + 1;
            while (j < textWithTashkeel.length) {
                const nextChar = textWithTashkeel[j];
                // If next char is NOT a main char (it's a tashkeel), include it.
                if (!mainCharRegex.test(nextChar) && nextChar !== '\u0671' && nextChar !== '\u0670' && nextChar !== ' ') {
                    j++;
                } else {
                    break;
                }
            }
            return j;
        }
    }
    return textWithTashkeel.length;
}

// for local debugging
function toUnicode(text) {
    let unicode = '';
    for (let i = 0; i < text.length; i++) {
        unicode += '\\u' + text.charCodeAt(i).toString(16).toUpperCase().padStart(4, '0');
    }
    return unicode;
}
// console.log(toUnicode("هَدَىٰكُمْ"));
// console.log(toUnicode(removeTashkeel("هَدَىٰكُمْ")));
// console.log(removeTashkeel('هَدَىٰكُمْ'));

export function applyIncorrectWordStyle(incorrectWord) {
    incorrectWord.classList.remove('correctWord');
    incorrectWord.classList.add('incorrectWord');
}

export function applyCorrectWordStyle(correctWord) {
    correctWord.classList.remove('incorrectWord');
    correctWord.classList.add('correctWord');

    // Unhide word if hidden due to hideWords button. (The working is none, delete hidden later)
    if (correctWord.style.visibility === 'hidden') {
        correctWord.style.visibility = "visible";
    }
}

/**
 * Gets the original offsetTop of the *first* element within the container.
 * This is used as a baseline to detect when content wraps to the next line.
 * @param {HTMLElement} container The container element (e.g., quranContainer).
 * @returns {number} The offsetTop value of the first child element, or 0 if the container is empty or the first child has no offsetTop.
 */
export function getOriginalTopOffset(container) {
    // Check if the container has any child nodes and the first child is an element with an offsetTop property
    if (container.firstChild && container.firstChild.offsetTop !== undefined) {
        // Return the offsetTop of the very first child element
        // This gives the vertical position of the beginning of the content.
        return container.firstChild.offsetTop;
    }

    // Return 0 or a default value if the container is empty or the first child isn't valid for offset calculation.
    // This prevents errors if the container is somehow empty when this function is called.
    console.warn("Could not determine originalTopOffset: Container might be empty or first child is not an element.");
    return 0;
}

export function handleHiddenWords(wordSpans, referenceSpan) {
    let foundReference = false;

    wordSpans.forEach((span) => {
        if (!foundReference) {
            if (span === referenceSpan) {
                foundReference = true;
            } else {
                span.style.display = 'none';
                // span.remove()
            }
        }
    });
}

export function clearContainer(container) {
    while (container.firstChild) {
        container.removeChild(container.firstChild);
    }
}

export function getTransitionDuration(element) {
    // Get the computed style of the element
    const style = window.getComputedStyle(element);

    // Extract the 'transition-duration' property value
    const transitionDuration = style.getPropertyValue('transition-duration');

    // Convert the string value to a number in milliseconds
    return parseFloat(transitionDuration) * 1000;
}

// Using this now for the tashkeel container.
export function fillContainer(surahContent, container) {
    clearContainer(container)

    // turn each word into a span
    const words = surahContent.split(" ")
    // console.log(words.join(" "));


    words.forEach((word) => {
        const wordSpan = document.createElement("span");
        wordSpan.textContent = `${word} `
        container.appendChild(wordSpan)

        // temp
        // console.log(word.split(""));
    });
}

export function initDarkMode(isDarkMode) {
    const root = document.documentElement; // Используем <html>
    if (isDarkMode) {
        root.classList.remove('light');
        root.classList.add('dark');
        // Обновляем иконки (если они все еще используются с таким id)
        const lightIcon = document.getElementById('light-mode-icon');
        const darkIcon = document.getElementById('dark-mode-icon');
        if (lightIcon) lightIcon.style.display = 'none';
        if (darkIcon) darkIcon.style.display = 'inline-block'; // Используем inline-block для img
    } else {
        root.classList.remove('dark');
        root.classList.add('light');
        const lightIcon = document.getElementById('light-mode-icon');
        const darkIcon = document.getElementById('dark-mode-icon');
        if (lightIcon) lightIcon.style.display = 'inline-block';
        if (darkIcon) darkIcon.style.display = 'none';
    }
    // Сохраняем начальное состояние в localStorage, если его нет
    if (localStorage.getItem('darkMode') === null) {
        localStorage.setItem('darkMode', isDarkMode ? 'enabled' : 'disabled');
    }
}

// Function to toggle dark mode
export function toggleDarkMode(isDarkMode) {
    const root = document.documentElement; // Используем <html>
    isDarkMode = !isDarkMode; // Переключаем состояние

    if (isDarkMode) {
        root.classList.remove('light');
        root.classList.add('dark');
        const lightIcon = document.getElementById('light-mode-icon');
        const darkIcon = document.getElementById('dark-mode-icon');
        if (lightIcon) lightIcon.style.display = 'none';
        if (darkIcon) darkIcon.style.display = 'inline-block';
    } else {
        root.classList.remove('dark');
        root.classList.add('light');
        const lightIcon = document.getElementById('light-mode-icon');
        const darkIcon = document.getElementById('dark-mode-icon');
        if (lightIcon) lightIcon.style.display = 'inline-block';
        if (darkIcon) darkIcon.style.display = 'none';
    }

    // Save the dark mode preference
    localStorage.setItem('darkMode', isDarkMode ? 'enabled' : 'disabled');
    return isDarkMode; // Возвращаем новое состояние
}

/**
 * Formats total elapsed milliseconds into HH:MM:SS.ms string format.
 * @param {number} elapsedMilliseconds - The total elapsed time in milliseconds.
 * @returns {string} The formatted time string (e.g., "00:01:30.550").
 */
export function formatTime(elapsedMilliseconds) {
    // Обработка случая, если передано не число или отрицательное значение
    if (isNaN(elapsedMilliseconds) || elapsedMilliseconds < 0) {
        elapsedMilliseconds = 0;
    }

    // Вычисляем компоненты времени
    const totalSeconds = Math.floor(elapsedMilliseconds / 1000);
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;
    const milliseconds = Math.floor(elapsedMilliseconds % 1000); // Используем floor для целых миллисекунд

    // Добавляем ведущие нули
    const formattedHours = String(hours).padStart(2, '0');
    const formattedMinutes = String(minutes).padStart(2, '0');
    const formattedSeconds = String(seconds).padStart(2, '0');
    // Форматируем миллисекунды до 3 знаков
    const formattedMilliseconds = String(milliseconds).padStart(3, '0');

    // Возвращаем отформатированную строку
    return `${formattedHours}:${formattedMinutes}:${formattedSeconds}.${formattedMilliseconds}`;
}

// ДОБАВИТЬ ЭТУ ФУНКЦИЮ
/**
 * Clamps a number between a minimum and maximum value.
 * @param {number} value The number to clamp.
 * @param {number} min The minimum allowed value.
 * @param {number} max The maximum allowed value.
 * @returns {number} The clamped number.
 */
export function clamp(value, min, max) {
    return Math.max(min, Math.min(value, max));
}

// ДОБАВИТЬ ЭТУ ФУНКЦИЮ
/**
 * Calculates Characters Per Minute (CPM).
 * @param {number} totalChars Total number of characters typed (or expected).
 * @param {number} elapsedMilliseconds Total elapsed time in milliseconds.
 * @returns {number} The calculated CPM. Returns 0 if time is 0.
 */
export function calculateCPM(totalChars, elapsedMilliseconds) {
    if (elapsedMilliseconds <= 0) {
        return 0; // Avoid division by zero or negative time
    }
    const timeInMinutes = elapsedMilliseconds / 60000; // Convert ms to minutes
    return totalChars / timeInMinutes;
}

// ДОБАВИТЬ ЭТУ ФУНКЦИЮ
/**
 * Calculates the Error Rate (ER) as a percentage.
 * @param {number} totalErrors Total number of errors made.
 * @param {number} totalChars Total number of characters typed (or expected).
 * @returns {number} The error rate percentage. Returns 0 if no characters were typed.
 */
export function calculateErrorRate(totalErrors, totalChars) {
    if (totalChars <= 0) {
        return 0; // Avoid division by zero
    }
    return (totalErrors / totalChars) * 100;
}

// ДОБАВИТЬ ЭТУ ФУНКЦИЮ
/**
 * Calculates the Adjusted CPM (aCPM) after applying penalty for errors.
 * @param {number} cpm The raw Characters Per Minute.
 * @param {number} totalErrors Total number of errors made.
 * @returns {number} The adjusted CPM, cannot be less than 0.
 */
export function calculateAdjustedCPM(cpm, totalErrors) {
    const penalty = totalErrors; // Penalty is 1 CPM per error
    return Math.max(0, cpm - penalty);
}

// ДОБАВИТЬ ЭТУ ФУНКЦИЮ
/**
 * Calculates the final score based on aCPM and a target CPM.
 * @param {number} aCPM The adjusted Characters Per Minute.
 * @param {number} targetCPM The target CPM for a 100% score.
 * @returns {number} The final score (0-100).
 */
export function calculateScore(aCPM, targetCPM) {
    if (targetCPM <= 0) {
        return 0; // Avoid division by zero if targetCPM is invalid
    }
    const rawScore = (aCPM / targetCPM) * 100;
    const roundedScore = Math.round(rawScore);
    return clamp(roundedScore, 0, 100); // Clamp the score between 0 and 100
}

// ДОБАВИТЬ ЭТУ ФУНКЦИЮ
/**
 * Determines the rank based on Score, aCPM, TargetCPM, and Error Rate.
 * @param {number} score The calculated score (0-100).
 * param {number} aCPM The adjusted Characters Per Minute.
 * param {number} targetCPM The target CPM.
 * @param {number} errorRate The calculated error rate percentage.
 * @returns {string} The rank ('S', 'A', 'B', 'C', 'D').
 */
export function determineRank(score, errorRate) {
    // if (targetCPM <= 0) return 'D'; // Default rank if targetCPM is invalid

    // const acpmRatio = aCPM / targetCPM; 

    // Check S rank first (most strict)
    // && acpmRatio >= 0.95
    if (score >= 95 && errorRate === 0) {
        return 'S';
    }
    // Check A rank
    // && acpmRatio >= 0.8 && acpmRatio < 0.95
    if (score >= 80 && score <= 94 && errorRate <= 1) {
        return 'A';
    }
    // Check B rank
    // && acpmRatio >= 0.6 && acpmRatio < 0.8 
    if (score >= 60 && score <= 79 && errorRate <= 3) {
        return 'B';
    }
    // Check C rank
    // && acpmRatio >= 0.4 && acpmRatio < 0.6
    if (score >= 40 && score <= 59 && errorRate <= 5) {
        return 'C';
    }
    // Default to D rank if none of the above conditions are met
    return 'D';
}

// Обновляем объект экспорта по умолчанию, чтобы включить новые функции
export default {
    convertToArabicNumber,
    createNoTashkeelString,
    removeTashkeel,
    getEndIndexInTashkeel,
    applyIncorrectWordStyle,
    applyCorrectWordStyle,
    getOriginalTopOffset,
    handleHiddenWords,
    clearContainer,
    getTransitionDuration,
    fillContainer,
    toggleDarkMode,
    initDarkMode,
    formatTime,
    clamp,
    calculateCPM,
    calculateErrorRate,
    calculateAdjustedCPM,
    calculateScore,
    determineRank,
};
```

### 2. src/css/styles.css

```css
/*------------------------------------*\
    #FONTS
\*------------------------------------*/
@font-face {
    font-family: 'IslamicFont';
    src: local('IslamicFont'),
         url('../../public/fonts/UthmaniHafs.woff') format('woff');
    font-display: swap; /* Improve perceived performance */
}

/* Apply special fonts */
.is-family-secondary,
#Quran-container,
#inputField,
#Surah-name, 
#Basmallah {
    font-family: 'IslamicFont', sans-serif;
    color: var(--input-text-color);
}

.logo-title {
    font-family: 'Dancing Script', cursive;
    color: var(--input-text-color);
}


/*------------------------------------*\
    #THEMING VARIABLES & BASE
\*------------------------------------*/
:root {
    /* Define custom properties for themes */
    --text-color: #111111;
    --background-color: #f5f5f5;
    --correct-word-color: #008000;
    --incorrect-word-color: #e10000;
    --link-color: #515154;
    --link-hover-color: #333333;
    --button-primary-bg: #1473e6;
    --button-primary-bg-hover: #0D66D0;
    --button-primary-text: #ffffff;
    --input-border-color: #d6d6d6;
    --input-background-color: #fafafa;
    --input-text-color: #111111;
    --input-placeholder-color: #838383;
    --footer-background-color: #eaeaea;
    --footer-text-color: var(--text-color);
    --footer-link-color: var(--link-color);
    --footer-link-hover-color: var(--link-hover-color);
}

:root.dark {
    --text-color: #ffffff;
    --background-color: #010101; /* Slightly off-black */
    --correct-word-color: #00e500;
    --incorrect-word-color: #ff8100;
    --link-color: #c7c7c7;
    --link-hover-color: #ffffff;
    --button-primary-bg: #1473e6; /* Can be same or different */
    --button-primary-bg-hover: #0D66D0;
    --button-primary-text: #ffffff;
    --input-border-color: #555; /* Darker border */
    --input-background-color: #1a1a1a; /* Dark input bg */
    --input-text-color: #ffffff;
    --input-placeholder-color: #aaa; /* Lighter placeholder */
    --footer-background-color: #202020; /* Dark footer background */
    --footer-text-color: var(--text-color);
    --footer-link-color: var(--link-color);
    --footer-link-hover-color: var(--link-hover-color);
}

html {
    background-color: var(--background-color);
    color: var(--text-color);
    transition: background-color 0.3s ease, color 0.3s ease;
    overflow: auto;
    /* Smooth scroll for better UX if needed */
    /* scroll-behavior: smooth; */
}

body {
    /* Prevent horizontal scrollbar if Bulma adds weird margins */
    overflow-x: hidden;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}


/*------------------------------------*\
    #BULMA OVERRIDES & CUSTOMIZATIONS
\*------------------------------------*/

/* Apply theme colors to Bulma elements */
.input, .textarea, .tag {
    background-color: var(--input-background-color);
    border-color: var(--input-border-color);
    color: var(--input-text-color);
    transition: background-color 0.3s ease, color 0.3s ease;
}

.input::placeholder, .textarea::placeholder {
    color: var(--input-placeholder-color);
}

.button.is-primary {
    background-color: var(--button-primary-bg);
    border-color: transparent; /* Often looks better */
    color: var(--button-primary-text);
}

.button.is-primary:hover, .button.is-primary:focus {
    background-color: var(--button-primary-bg-hover);
    color: var(--button-primary-text); /* Ensure text color stays */
}

a, .footer-link {
    color: var(--link-color);
}

a:hover, .footer-link:hover {
    color: var(--link-hover-color);
}

.footer {
    background-color: var(--footer-background-color);
    color: var(--footer-text-color);
    font-family: sans-serif;
}

.footer a {
    color: var(--footer-link-color);
}
.footer a:hover {
    color: var(--footer-link-hover-color);
}

/* Correct/Incorrect word styling */
#Quran-container .correctWord {
    color: var(--correct-word-color);
    /* transition: color 0.1s ease-in-out; */
}

#Quran-container .incorrectWord {
    color: var(--incorrect-word-color);
    /* Optional: add subtle background or underline for more emphasis */
    background-color: rgba(255, 0, 0, 0.15);
    /* transition: color 0.1s ease-in-out; */
}

/* --- NEW: Character Level Highlighting --- */
.correct-char {
    color: var(--correct-word-color);
}

/* Cursor Effect for the current word */
@keyframes blink {
    0% { border-left-color: var(--button-primary-bg); }
    50% { border-left-color: transparent; }
    100% { border-left-color: var(--button-primary-bg); }
}

.cursor-active {
    /* Add a blinking border to the left (since RTL) of the current word */
    border-left: 2px solid var(--button-primary-bg);
    /* animation: blink 1s step-end infinite; */ /* Optional blinking */
    padding-left: 2px;
}


/*------------------------------------*\
    #COMPONENT STYLING
\*------------------------------------*/

/* Quran Container */
#Quran-container {
    /* Adjust height based on desired number of lines & font size */
    /* Example: Roughly 4 lines with 34px font and Bulma line-height */
    height: 220px;
    overflow: hidden; /* Keep hidden to manage scroll behavior via JS */
    max-width: 800px; /* Match original */
    margin-right: auto; /* Center in container */
    margin-left: auto;
    font-size: 34px; /* Original font size */
    line-height: 1.6; /* Adjust line-height for readability */
    padding: 10px;
    cursor: text; /* Indicate it's clickable to focus */
}

#Quran-container span {
    /* Ensure proper spacing between words if needed */
    margin-left: 0.2em; /* Adjust spacing for RTL */
     display: inline-block; /* Ensures visibility toggling works reliably */
}

/* Main Input Field - HIDDEN BUT FUNCTIONAL */
#inputField {
    opacity: 0;
    position: absolute;
    z-index: -1;
    height: 0;
    width: 0;
    padding: 0;
    border: none;
}

#Quran-input-container .field {
     width: 100%; /* Make the group take full width */
     max-width: 700px; /* Control max width of input+button group */
}


/* Hide Ayahs Button */
#hideAyahsButton {
    height: 65px; /* Match input field height */
    align-self: stretch; /* Ensure button stretches vertically in group */
}

/* Repetition Controls */
.repetition-input {
    width: 65px; /* Fixed width for number inputs */
    text-align: center;
}
/* Remove spinners from number input */
.repetition-input[type=number]::-webkit-inner-spin-button,
.repetition-input[type=number]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
/* .repetition-input[type=number] { */
  /* -moz-appearance: textfield; Firefox */
/* } */


/* Стили для кнопок с изображениями */
.image-button {
    background: none !important; /* Убираем фон */
    border: none !important; /* Убираем рамку */
    padding: 0.5rem; /* Добавляем немного отступа вокруг иконки для кликабельности */
    cursor: pointer;
    line-height: 0; /* Предотвращаем влияние высоты строки на размер кнопки */
    transition: background-color 0.2s ease-in-out; /* Плавный переход для hover */
}

.image-button:hover,
.image-button:focus {
    background-color: var(--input-border-color) !important;
    outline: none;
}

/* Стили для самих иконок внутри кнопок */
.button-icon {
    width: 24px;
    height: 24px;
    vertical-align: middle;
}

/* Переопределяем размер иконки темы, если он отличается */
#dark-mode-toggle .button-icon {
    width: 24px;
    height: 24px;
}

html.light #dark-mode-icon { display: none; }
html.light #light-mode-icon { display: inline-block; }
html.dark #light-mode-icon { display: none; }
html.dark #dark-mode-icon { display: inline-block; }

html.light #dark-menu-icon { display: none; }
html.light #light-menu-icon { display: inline-block; }
html.dark #light-menu-icon { display: none; }
html.dark #dark-menu-icon { display: inline-block; }

/* Footer */
.footer {
    padding-top: 2rem;
    padding-bottom: 2rem;
    transition: background-color 0.3s ease, color 0.3s ease;
}
#errorCounterContainer {
    color: var(--incorrect-word-color);
    white-space: nowrap; /* Prevent wrapping */
}

/* Добавь это в конец файла или в секцию Footer */
#timerContainer {
    color: var(--text-color); /* Используем цвет текста темы */
    white-space: nowrap; /* Предотвращаем перенос строки */
}

#timerDisplay {
     /* Можно добавить акцентный цвет, если хочешь */
     color: var(--button-primary-bg);
}

/*------------------------------------*\
    #UTILITIES
\*------------------------------------*/
.is-sr-only { /* Screen Reader Only - Bulma has .is-sr-only */
    position: absolute !important;
    clip: rect(1px, 1px, 1px, 1px);
    padding: 0 !important;
    border: 0 !important;
    height: 1px !important;
    width: 1px !important;
    overflow: hidden;
    white-space: nowrap;
}
.is-fullwidth {
    width: 100%;
}


/*------------------------------------*\
    #RESPONSIVE ADJUSTMENTS
\*------------------------------------*/
@media screen and (max-width: 768px) { /* Bulma's tablet breakpoint */
    .level-left + .level-right {
        margin-top: 1rem; /* Add space when level items stack */
    }
    #Quran-container {
        font-size: 28px; /* Slightly smaller font on mobile */
        height: 190px; /* Adjust height */
    }
    #inputField {
        font-size: 28px; /* Match Quran font size */
        height: 55px; /* Adjust height */
    }
     #hideAyahsButton {
        height: 55px; /* Match input height */
    }

    /* Stack footer items */
    .footer .level {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
    }
    .footer .level-item {
         margin: 0 !important; /* Reset level item margins */
    }
}

@media screen and (max-width: 500px) {
     .level:not(.is-mobile) .level-item { /* Ensure search/toggle stack */
         margin-right: 0;
         margin-bottom: 0.75rem;
     }
     .level:not(.is-mobile) .level-item:last-child {
         margin-bottom: 0;
     }
     #Quran-input-container.is-grouped { /* Stack input and button */
         flex-direction: column;
         align-items: stretch; /* Make items full width */
     }
     #Quran-input-container .control {
         width: 100%; /* Make controls full width */
     }
      #Quran-input-container .control:not(:last-child) {
         margin-bottom: 0.75rem; /* Add space when stacked */
     }
     #inputField {
        max-width: none; /* Allow full width */
     }
      #repetitionControlsRow.is-grouped {
         flex-direction: column; /* Stack repetition controls */
          gap: 0.75rem;
     }
}

/* Toastify Customization (Optional) */
.toastify {
  padding: 12px 20px;
  color: #fff;
  display: inline-block;
  box-shadow: 0 3px 6px -1px rgba(0, 0, 0, 0.12), 0 10px 36px -4px rgba(77, 96, 232, 0.3);
  background: linear-gradient(to right, #1473e6, #0D66D0); /* Match button color */
  position: fixed;
  opacity: 0;
  transition: all 0.4s cubic-bezier(0.215, 0.61, 0.355, 1);
  border-radius: 4px; /* Match Bulma radius */
  cursor: pointer;
  text-decoration: none;
  max-width: calc(50% - 20px);
  z-index: 9999; /* Bulma uses 30 for navbar, 40 for modal. Keep high */
}

/* RTL adjustments for Toastify if needed */
html[dir="rtl"] .toastify.on.toastify-right {
    right: auto;
    left: 15px;
}
html[dir="rtl"] .toastify.on.toastify-left {
    left: auto;
    right: 15px;
}

/*-------------------------------------------*\\
    # SELECTION TABLE THEME ADAPTATION
\\*------------------------------------------*/
.selection-table tbody tr {
    cursor: pointer; /* Показывает, что строка кликабельна */
}

/* Общие стили таблицы */
.selection-table {
    background-color: var(--background-color); /* Основной фон таблицы = фон страницы */
    color: var(--text-color); /* Основной цвет текста */
}

/* Стили заголовка таблицы (thead) */
.selection-table thead {
    background-color: var(--input-background-color); /* Фон заголовка чуть темнее/светлее фона */
    border-bottom: 2px solid var(--input-border-color); /* Четкая линия под заголовком */
}

.selection-table thead th {
    color: var(--text-color); /* Цвет текста в заголовке */
    border-color: var(--input-border-color); /* Цвет границ ячеек заголовка */
    border-width: 0 0 2px 1px; /* Убираем верхнюю/правую, задаем нижнюю/левую */
    vertical-align: middle; /* Выравнивание по центру */
}
.selection-table thead th:first-child {
     border-left-width: 0; /* Убираем левую границу у первой ячейки */
}


/* Стили тела таблицы (tbody) */
.selection-table tbody td {
    color: var(--text-color); /* Цвет текста в ячейках */
    border-color: var(--input-border-color); /* Цвет границ ячеек */
    vertical-align: middle; /* Выравнивание по центру */
}

/* Адаптация для is-bordered */
.selection-table.is-bordered th,
.selection-table.is-bordered td {
    border-color: var(--input-border-color);
}

.table.is-striped tbody tr:nth-child(1n) {
    /* Явно задаем основной фон для нечетных строк */
     background-color: var(--background-color) !important;
}

/* Адаптация для is-striped (чередующиеся строки) */
.table.is-striped tbody tr:nth-child(2n) {
    /* Используем цвет фона инпутов для чередования */
    background-color: var(--input-background-color) !important;
}

/* Новый стиль :hover, использующий переменные */
.selection-table.is-hoverable tbody tr:hover {
    /* Используем цвет фона футера или другой подходящий для выделения */
    background-color: var(--footer-background-color) !important; /* Используем !important для переопределения Bulma */
    /* Убедимся, что текст читаем при наведении */
    /* Можно оставить --text-color или использовать --footer-text-color, если он отличается */
    color: var(--text-color) !important;
}

/* Стиль для контейнера таблицы (ограничение высоты и прокрутка) */
#surah-selection-section .table-container {
    max-height: 65vh;
    overflow-y: auto;
    border: 1px solid var(--input-border-color); /* Добавляем границу к контейнеру */
    border-radius: 6px; /* Скругляем углы контейнера (как у Bulma card/input) */
}

/* Убираем стандартную границу у самой таблицы внутри контейнера, если есть */
#surah-selection-section .table-container .table {
    border: none; /* Убираем границу, если она есть у table */
}

/* Для Firefox */
#surah-selection-section .table-container {
    scrollbar-width: thin; /* Делаем скроллбар тонким (альтернативы: 'auto', 'none') */
    /* Задаем цвет ползунка и фона скроллбара, используя переменные темы */
    scrollbar-color: var(--button-primary-bg) var(--input-background-color);
}

/* Для WebKit браузеров (Chrome, Safari, Edge, Opera) */

/* Общий контейнер скроллбара */
#surah-selection-section .table-container::-webkit-scrollbar {
    width: 8px;  /* Ширина вертикального скроллбара */
    height: 8px; /* Высота горизонтального скроллбара (если появится) */
}

/* Фон (дорожка) скроллбара */
#surah-selection-section .table-container::-webkit-scrollbar-track {
    background: var(--input-background-color); /* Цвет фона, чуть отличающийся от основного */
    border-radius: 4px; /* Небольшое скругление углов */
    /* border: 1px solid var(--input-border-color); */ /* Опциональная рамка */
}

/* Ползунок скроллбара */
#surah-selection-section .table-container::-webkit-scrollbar-thumb {
    background-color: var(--button-primary-bg); /* Основной цвет ползунка (как у кнопок) */
    border-radius: 4px; /* Скругление углов, как у дорожки */
    /* Создаем эффект отступа с помощью рамки цвета фона дорожки */
    border: 2px solid var(--input-background-color);
}

/* Ползунок скроллбара при наведении */
#surah-selection-section .table-container::-webkit-scrollbar-thumb:hover {
    background-color: var(--button-primary-bg-hover); /* Цвет при наведении (как у кнопок) */
}

/* Опционально: Углы (если есть и горизонтальный и вертикальный скроллбар) */
#surah-selection-section .table-container::-webkit-scrollbar-corner {
  background: var(--input-background-color); /* Цвет угла */
}

/*------------------------------------*\\
    # TAB STYLING (Остается без изменений)
\\*------------------------------------*/

/* Скрытие неактивного контента вкладок */
.tab-content.is-hidden {
    display: none;
}

/* Адаптация вкладок под тему */
.tabs.is-boxed li.is-active a {
    background-color: var(--background-color); /* Фон активной вкладки */
    border-color: var(--input-border-color);
    border-bottom-color: transparent !important; /* Убираем нижнюю границу */
}
.tabs.is-boxed a {
    border-color: var(--input-border-color);
    color: var(--link-color);
}
.tabs.is-boxed a:hover {
    background-color: var(--input-background-color); /* Фон при наведении */
    border-bottom-color: var(--input-border-color) !important;
    color: var(--link-hover-color);
}
.tabs ul {
    border-bottom-color: var(--input-border-color) !important;
}

.selection-table .start-segment-button:hover {
     background-color: var(--input-background-color); /* Слегка выделяем фон */
}

/* Убедимся, что вертикальное выравнивание в таблицах выбора хорошее */
.selection-table tbody td {
    vertical-align: middle;
}
```

### 3. src/js/logic.js

```javascript
import utils from './utils.js';

const BASMALLA = "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ"
// Added ayah marker start '﴿' to the list for easier checking
const QURAN_SYMBOLS = ["۞", "﴾", "﴿", "۩", 'ۖ', 'ۗ', 'ۘ', 'ۙ', 'ۚ', ' ۛ', 'ۜ', 'ۛ ']
let PROPERTIES_OF_SURAHS = null
const TARGET_CPM = 400;

// --- Constants for Segment Types ---
const SEGMENT_TYPE = {
    SURAH: 'surah',
    JUZ: 'juz',
    HIZB: 'hizb',
    RUB: 'rub',
    PAGE: 'page',
    SEARCH: 'search'
};

// --- Constants for Segment Counts ---
const COUNT = {
    JUZ: 30,
    HIZB: 60,
    RUB: 240,
    PAGE: 604
};

// --- UI State ---
// Определяем предпочтения пользователя ИЛИ сохраненное значение
const prefersDarkMode = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
const savedMode = localStorage.getItem('darkMode');
let isDarkMode = savedMode === 'enabled' || (savedMode === null && prefersDarkMode);
let isHideAyahsButtonActive = false
let currentSearchQuery = null; // Initialize to null to ensure first load happens

// --- Typing State ---
let currentLetterIndex = 0 // Tracks letter index within a word (might be less relevant with word comparison)
let mainQuranWordIndex = 0 // Index for the main container (with symbols)
let noTashkeelWordIndex = 0 // Index for the hidden no-tashkeel container

// --- Ayah Repetition State ---
let ayahRepeatCount = 1; // How many times to repeat the current ayah (renamed for clarity)
let currentAyahRepetition = 1; // Which repetition we are currently on for the current ayah
let currentAyahStartIndex_Main = 0; // Start index of the current ayah in the main container
let currentAyahStartIndex_NoTashkeel = 0; // Start index of the current ayah in the no-tashkeel container

// --- Word Repetition State ---
let wordRepeatCount = 1; // How many times to repeat the current word
let currentWordRepetition = 1; // Which repetition we are currently on for the current word

// --- Error Tracking ---
let totalErrors = 0; // Cumulative errors for the current Surah/Ayah segment

// --- Timer State ---
let timerInterval = null; // Stores the interval ID for the timer
let startTime = null;  // Stores the timestamp when the timer started
let endTime = null; // Stores the timestamp when the timer stopped
let timerDisplayElement = null; // Cache timer display element

// --- Auto-Scroll Detection State ---
let originalTopOffset = 0 // Top offset of the first line
let secondRowTopOffset = 0 // Top offset of the second line (once it appears)
let refWord = null // Reference word span used for hiding previous lines

// --- Ranking & Selection State ---
let currentMode = 'normal'; // 'normal' or 'blind'
let currentSelectionType = SEGMENT_TYPE.SURAH; // 'surah', 'juz', 'hizb', 'rub', 'page', 'search'
let currentSelectionId = null; // ID текущего сегмента (номер суры, джуза и т.д.)
const RESULTS_STORAGE_KEY = 'quranTypePlusResults';
let totalCharsInSegment = 0;
let acpmDisplay = null;
let scoreDisplay = null;
let rankDisplay = null;

// --- DOM Element References (Cache frequently used elements) ---
let quranContainer = null;
let noTashkeelContainer = null;
let inputElement = null;
let errorCountDisplay = null;
let repeatCountInput = null;
let wordRepeatCountInput = null;
let surahSelectionSection = null;
let mainTypingSection = null;
let surahSelectionTBody = null;
let changeSurahButton = null;
let hideAyahsButton = null;
// ДОБАВЛЕНО: Ссылки на tbody для новых таблиц
let juzSelectionTBody = null;
let hizbSelectionTBody = null;
let rubSelectionTBody = null;
let pageSelectionTBody = null;
// ДОБАВЛЕНО: Ссылки на контейнеры вкладок и сами вкладки
let tabLinks = null;
let tabContentContainers = null;

// --- Initialization Functions ---

/**
 * Caches frequently accessed DOM elements.
 */
function cacheDOMElements() {
    quranContainer = document.getElementById("Quran-container");
    noTashkeelContainer = document.getElementById("noTashkeelContainer");
    inputElement = document.getElementById("inputField");
    errorCountDisplay = document.getElementById("errorCountDisplay"); // Cache error display
    repeatCountInput = document.getElementById('repeatCountInput');
    wordRepeatCountInput = document.getElementById('wordRepeatCountInput'); // Cache word repeat input
    timerDisplayElement = document.getElementById("timerDisplay");
    surahSelectionSection = document.getElementById('surah-selection-section');
    mainTypingSection = document.getElementById('main-typing-section');
    changeSurahButton = document.getElementById('change-surah-button');
    hideAyahsButton = document.getElementById('hideAyahsButton');
    acpmDisplay = document.getElementById("acpmDisplay");
    scoreDisplay = document.getElementById("scoreDisplay");
    rankDisplay = document.getElementById("rankDisplay");

    // ДОБАВЛЕНО: Кэширование tbody для всех таблиц
    surahSelectionTBody = document.getElementById('surah-selection-tbody');
    juzSelectionTBody = document.getElementById('juz-selection-tbody');
    hizbSelectionTBody = document.getElementById('hizb-selection-tbody');
    rubSelectionTBody = document.getElementById('rub-selection-tbody');
    pageSelectionTBody = document.getElementById('page-selection-tbody');

    // ДОБАВЛЕНО: Кэширование элементов вкладок
    tabLinks = document.querySelectorAll('.tabs li[data-tab]');
    tabContentContainers = document.querySelectorAll('.tab-content');
}

/**
 * Fetches properties of all Surahs (like names, bismillah presence) from the API.
 */
async function setupSurahData() {
    const baseApiUrl = 'https://api.quran.com/api/v4';
    const url = `${baseApiUrl}/chapters`;

    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Failed to fetch surah data');
        }
        PROPERTIES_OF_SURAHS = await response.json();
    } catch (error) {
        console.error('Error fetching surah data:', error);
        // Potentially show error to user
    }
}

// ИЗМЕНЕНО: Создаем общую функцию для загрузки сегментов
/**
 * Fetches and displays a specific Quran segment (Surah, Juz, Hizb, etc.).
 * Resets state variables for the new segment.
 * @param {string} type - The type of segment (use SEGMENT_TYPE constants).
 * @param {number} id - The number of the segment (Surah number, Juz number, etc.).
 * @param {string} script - The Quran script to use (e.g., 'uthmani').
 */
async function getQuranSegment(type, id, script) {
    // --- Reset State for New Segment ---
    resetTimer();
    currentLetterIndex = 0;
    mainQuranWordIndex = 0;
    noTashkeelWordIndex = 0;

    currentAyahRepetition = 1; // Reset ayah repetition count
    currentWordRepetition = 1; // Reset word repetition count

    currentAyahStartIndex_Main = 0;
    currentAyahStartIndex_NoTashkeel = 0;

    totalErrors = 0; // Reset error count
    updateErrorDisplay(); // Update the display to show 0 errors

    totalCharsInSegment = 0;
    resetResultsDisplay();

    originalTopOffset = 0;
    secondRowTopOffset = 0;
    refWord = null;

    inputElement.value = ""; // Clear input field
    inputElement.classList.remove('incorrectWord'); // Ensure input isn't styled incorrectly initially
    inputElement.disabled = false; // Ensure input is enabled

    // Reset hide words state visually if needed (e.g., button text)
    // if (isHideAyahsButtonActive) { handleHideAyahsButton(); } // Toggle off if desired

    // Сохраняем тип и ID текущего выбора
    currentSelectionType = type;
    currentSelectionId = id;

    // Constructing the API URL based on type
    const baseApiUrl = 'https://api.quran.com/api/v4';
    let url = `${baseApiUrl}/quran/verses/${script}?`;
    let segmentName = ''; // Для отображения информации о сегменте

    switch (type) {
        case SEGMENT_TYPE.SURAH:
            // Добавляем обработку случая, когда ID содержит ':' (для поиска)
            let surahNum = id, startAyah = 1;
            if (typeof id === 'string' && id.includes(':')) {
                const parts = id.split(':');
                surahNum = parseInt(parts[0], 10);
                startAyah = parseInt(parts[1], 10) || 1;
                // Обновляем currentSelectionId, если он был строкой
                currentSelectionId = surahNum; // Для сохранения результатов используем только номер суры
            } else {
                surahNum = parseInt(id, 10);
            }
            url += `chapter_number=${surahNum}`;
            // Получаем имя суры позже, после загрузки данных
            break;
        case SEGMENT_TYPE.JUZ:
            url += `juz_number=${id}`;
            segmentName = `Juz ${utils.convertToArabicNumber(id)}`;
            break;
        case SEGMENT_TYPE.HIZB:
            url += `hizb_number=${id}`;
            segmentName = `Hizb ${utils.convertToArabicNumber(id)}`;
            break;
        case SEGMENT_TYPE.RUB:
            url += `rub_el_hizb_number=${id}`;
            segmentName = `Rub' ${utils.convertToArabicNumber(id)}`;
            break;
        case SEGMENT_TYPE.PAGE:
            url += `page_number=${id}`;
            segmentName = `Page ${utils.convertToArabicNumber(id)}`;
            break;
        default:
            showToast("Invalid selection type.");
            return;
    }

    // Show loading indicator (optional)
    // showLoadingIndicator(true);

    try {
        const response = await fetch(url);
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({})); // Попытка получить тело ошибки
            throw new Error(`Failed to fetch verses for ${type} ${id}. Status: ${response.status}. ${errorData.message || ''}`);
        }
        const data = await response.json();

        // --- Обработка старта не с первого аята для Сур ---
        let effectiveStartAyah = 1;
        let displayData = data;
        let chapterInfo = null;

        if (type === SEGMENT_TYPE.SURAH || currentSelectionType === SEGMENT_TYPE.SEARCH) {
            let surahNumToUse = currentSelectionId; // Используем сохраненный номер суры
            chapterInfo = PROPERTIES_OF_SURAHS?.chapters?.[surahNumToUse - 1];

            // Обрабатываем случай, когда ID содержал номер аята
            if (typeof id === 'string' && id.includes(':')) {
                const parts = id.split(':');
                effectiveStartAyah = parseInt(parts[1], 10) || 1;
            } else {
                effectiveStartAyah = 1; // По умолчанию для суры, если не указан аят
            }

            const totalAyahs = data.verses.length;
            // Validate startAyah only for Surah type fetched by chapter_number
            if (effectiveStartAyah < 1) {
                effectiveStartAyah = 1;
            } else if (effectiveStartAyah > totalAyahs) {
                const surahName = chapterInfo?.name_simple || `Surah ${surahNumToUse}`;
                showToast(`${surahName} only contains ${utils.convertToArabicNumber(totalAyahs)} ayahs. Starting from Ayah ${utils.convertToArabicNumber(1)}.`);
                effectiveStartAyah = 1;
            }
            // Обрезаем данные для суры, если нужно начать не с 1 аята
            displayData = processData(data, effectiveStartAyah, script);
        } else {
            // Для Juz, Hizb и т.д. API уже возвращает нужный сегмент, startAyah не нужен
            effectiveStartAyah = 1; // Считаем, что для этих сегментов всегда начинаем с "первого" аята сегмента
            // Определяем информацию о главе из первого аята полученных данных (для басмалы)
            const firstVerseKey = data.verses[0]?.verse_key;
            if (firstVerseKey) {
                const firstVerseParts = firstVerseKey.split(':');
                const chapterNumberOfFirstVerse = parseInt(firstVerseParts[0], 10);
                const ayahNumberOfFirstVerse = parseInt(firstVerseParts[1], 10);
                chapterInfo = PROPERTIES_OF_SURAHS?.chapters?.[chapterNumberOfFirstVerse - 1];
                // Показываем басмалу только если сегмент начинается с 1-го аята суры (кроме 9-й)
                if (ayahNumberOfFirstVerse !== 1 || chapterNumberOfFirstVerse === 9 || chapterNumberOfFirstVerse === 1) {
                    chapterInfo = { ...chapterInfo, bismillah_pre: false }; // Переопределяем для случая не первого аята
                }
            }
        }


        applyModeSettings(); // Применяем настройки режима (например, скрыть кнопку)
        // Передаем displayData, effectiveStartAyah и segmentName/chapterInfo
        displaySegmentFromJson(displayData, effectiveStartAyah, script, type, chapterInfo, segmentName);

    } catch (error) {
        console.error('Error fetching verses:', error);
        showToast(`Error fetching data for ${type} ${id}. Please try again.`);
        inputElement.disabled = true;
    } finally {
        console.log(currentMode);
        applyModeSettings();
        if (inputElement && !mainTypingSection.classList.contains('is-hidden')) {
            inputElement.disabled = false;
            inputElement.focus();
        }
    }
}

/**
 * Applies UI settings based on the current mode (currentMode).
 * Primarily hides/shows the "Hide Ayahs" button.
 */
function applyModeSettings() {
    if (!hideAyahsButton) return; // Ensure button exists

    if (currentMode === 'blind') {
        hideAyahsButton.style.display = 'none'; // Hide in blind mode
        // Ensure text is NOT hidden if switching to blind mode
        // after activating Hide in normal mode
        if (!isHideAyahsButtonActive) {
            handleHideAyahsButton(); // "Click" button to hide ayahs
        }
    } else { // currentMode === 'normal' or 'search'
        hideAyahsButton.style.display = ''; // Show in normal/search mode
        // Button state (pressed/not pressed) is maintained by isHideAyahsButtonActive
        // and applied by applyHideAyahsVisibility if needed
    }
}

// --- Data Processing and Display ---

/**
 * Processes the raw ayah text (e.g., handling iqlab).
 * @param {string} text - The raw ayah text.
 * @returns {string} The processed ayah text.
 */
function processAyah(text) {
    let ayah = text;
    // Handle iqlab if necessary for comparison logic (may not be needed depending on removeTashkeel)
    ayah = ayah.replace(/\u064B\u06E2/g, '\u064E\u06E2');
    ayah = ayah.replace(/\u064C\u06E2/g, '\u064F\u06E2');
    ayah = ayah.replace(/\u064D\u06ED/g, '\u0650\u06ED');
    return ayah;
}

/**
 * Prepares the verse data: trims whitespace, slices based on startAyah (only for Surah type).
 * @param {object} data - The raw API response data.
 * @param {number} startAyah - The ayah number to start from (relevant for Surah).
 * @param {string} script - The script type.
 * @returns {object} The processed data object (potentially sliced).
 */
function processData(data, startAyah, script) {
    // Trim initial space if present
    const textProp = `text_${script}`;
    if (data.verses.length > 0 && data.verses[0][textProp]?.startsWith(' ')) {
        data.verses[0][textProp] = data.verses[0][textProp].trim();
    }
    // Slice only if startAyah > 1 (relevant for Surah type)
    if (startAyah > 1) {
        // Create a deep copy to avoid modifying the original data if it's cached elsewhere
        const slicedData = JSON.parse(JSON.stringify(data));
        slicedData.verses = slicedData.verses.slice(startAyah - 1);
        return slicedData;
    }
    return data; // Return original data if starting from Ayah 1
}


// ИЗМЕНЕНО: Обобщенная функция отображения
/**
 * Displays the fetched segment content and sets up related elements.
 * @param {object} data - The processed API response data for the segment.
 * @param {number} startAyah - The effective starting ayah number within the segment/surah.
 * @param {string} script - The script type.
 * @param {string} type - The type of segment displayed (SEGMENT_TYPE).
 * @param {object | null} chapterInfo - Info about the Surah (relevant for name/basmallah).
 * @param {string} segmentName - Name of the segment (e.g., "Juz 1").
 */
function displaySegmentFromJson(data, startAyah, script, type, chapterInfo, segmentName) {
    const surahNameEl = document.getElementById("Surah-name");
    const basmallahContainer = document.getElementById("Basmallah");

    const noTashkeelAyahs = [];
    let firstVerseActualNumber = -1; // Для определения первого аята в сегменте

    const surahContent = data.verses.map((ayah, i) => {
        const verseKeyParts = ayah.verse_key.split(':');
        const currentAyahNumberInSurah = parseInt(verseKeyParts[1], 10);
        if (i === 0) {
            firstVerseActualNumber = currentAyahNumberInSurah;
        }
        const arabicNumber = utils.convertToArabicNumber(currentAyahNumberInSurah);
        const processedAyah = processAyah(ayah[`text_${script}`]);
        noTashkeelAyahs.push(processedAyah);
        return `${processedAyah} ﴿${arabicNumber}﴾`;
    }).join(" ");

    // Set Surah Name/Segment Name
    if (type === SEGMENT_TYPE.SURAH || type === SEGMENT_TYPE.SEARCH) {
        surahNameEl.textContent = chapterInfo ? `سورة ${chapterInfo.name_arabic}` : '';
    } else {
        surahNameEl.textContent = segmentName || ''; // Отображаем имя джуза, хизба и т.д.
    }

    // Set Basmallah
    // Показываем басмалу, если:
    // 1. Это Сура (или поиск) И начинается с 1 аята И есть флаг bismillah_pre
    // 2. Это НЕ Сура (Джуз, Хизб и т.д.) И сегмент начинается с 1 аята суры (проверено в getQuranSegment) И есть флаг bismillah_pre
    if (chapterInfo?.bismillah_pre && ((type === SEGMENT_TYPE.SURAH || type === SEGMENT_TYPE.SEARCH) && startAyah === 1 || (type !== SEGMENT_TYPE.SURAH && type !== SEGMENT_TYPE.SEARCH && firstVerseActualNumber === 1))) {
        basmallahContainer.textContent = BASMALLA;
    } else {
        basmallahContainer.textContent = "";
    }

    // Ensure fonts are ready before filling containers and calculating offsets
    document.fonts.ready.then(() => {
        fillContainerWithSpans(surahContent, quranContainer);

        const noTashkeelString = utils.createNoTashkeelString(noTashkeelAyahs);
        utils.fillContainer(noTashkeelString, noTashkeelContainer);

        // Calculate total characters for CPM
        totalCharsInSegment = noTashkeelString.replace(/\s/g, '').length;

        // Calculate initial scroll offsets
        originalTopOffset = utils.getOriginalTopOffset(quranContainer);
        secondRowTopOffset = 0;
        refWord = null;

        const wordSpans = quranContainer.querySelectorAll('span');
        if (wordSpans.length > 0) {
            refWord = wordSpans[0]; // Initialize refWord to the first word
            // Add cursor to first word
            refWord.classList.add('cursor-active');
            
            for (let i = 1; i < wordSpans.length; i++) {
                const span = wordSpans[i];
                if (span.offsetTop > originalTopOffset) {
                    secondRowTopOffset = span.offsetTop;
                    refWord = span; // Update refWord if second line found immediately
                    break;
                }
            }
        }
        // Reset ayah start indices
        currentAyahStartIndex_Main = 0;
        currentAyahStartIndex_NoTashkeel = 0;

        applyModeSettings(); // Apply mode settings (e.g., hide button)

        // Apply initial hide state if active (only in normal/search mode)
        if (isHideAyahsButtonActive) {
            applyHideAyahsVisibility();
        }

        // Focus input field if ready
        if (inputElement && !mainTypingSection.classList.contains('is-hidden')) {
            inputElement.disabled = false;
            inputElement.focus();
        }
    });
}

/**
 * Fills a container with spans, one for each word.
 * @param {string} content - The text content.
 * @param {HTMLElement} container - The container element to fill.
 */
function fillContainerWithSpans(content, container) {
    utils.clearContainer(container);
    // Reset scroll offsets before filling
    originalTopOffset = 0;
    secondRowTopOffset = 0;
    refWord = null;

    const words = content.split(" ");
    words.forEach((word) => {
        if (word) { // Avoid creating spans for empty strings from multiple spaces
            const span = document.createElement('span');
            span.textContent = `${word} `; // Add space back for rendering
            // Store original text for highlighting logic
            span.dataset.originalText = `${word} `;
            container.appendChild(span);
        }
    });
    // Recalculate original offset *after* filling
    originalTopOffset = utils.getOriginalTopOffset(container);
    // Find second row offset immediately if needed (although it's also done in displaySegmentFromJson)
    const wordSpans = container.querySelectorAll('span');
    if (wordSpans.length > 0) {
        refWord = wordSpans[0];
        for (let i = 1; i < wordSpans.length; i++) {
            if (wordSpans[i].offsetTop > originalTopOffset) {
                secondRowTopOffset = wordSpans[i].offsetTop;
                refWord = wordSpans[i];
                break;
            }
        }
    }
}


// --- Input Handling and Logic (Без существенных изменений) ---
/**
 * Handles the 'input' event on the text field. Compares input with the expected text.
 * Increments error counter on mismatch.
 * @param {Event} event - The input event object.
 */
function handleInput(event) {
    if (startTime === null) {
        startTimer();
    }

    const wordSpans = quranContainer.querySelectorAll('span');
    if (noTashkeelWordIndex >= noTashkeelContainer.childNodes.length || mainQuranWordIndex >= wordSpans.length) {
        return;
    }

    // Защита от ошибки, если узел не текстовый (маловероятно, но возможно)
    if (noTashkeelContainer.childNodes[noTashkeelWordIndex].nodeType !== Node.TEXT_NODE && !noTashkeelContainer.childNodes[noTashkeelWordIndex].textContent) {
        console.warn("Unexpected node type or missing text content in noTashkeelContainer at index", noTashkeelWordIndex);
        inputElement.disabled = true; // Блокируем ввод для предотвращения дальнейших ошибок
        showToast("Internal error: Text mismatch. Please reload.");
        return;
    }

    const currentNoTashkeelWord = noTashkeelContainer.childNodes[noTashkeelWordIndex].textContent;
    const inputText = event.target.value;
    const targetWordSpan = wordSpans[mainQuranWordIndex];
    if (!targetWordSpan) return; // Доп. проверка

    // Handle Spacebar (Word Submission)
    // If input ends with space, check if the word is complete
    if (inputText.endsWith(' ') || (event.data === ' ' && inputText.trim().length > 0)) {
        const trimmedInput = inputText.trim();
        const trimmedTarget = currentNoTashkeelWord.trim();
        
        if (trimmedInput === trimmedTarget) {
            handleCorrectWord(wordSpans);
            return;
        }
    }

    if (currentNoTashkeelWord.startsWith(inputText)) {
        targetWordSpan.classList.remove('incorrectWord');
        
        // --- Character Highlighting Logic ---
        updateCurrentWordHighlighting(targetWordSpan, inputText.length);

        if (inputText === currentNoTashkeelWord) {
            handleCorrectWord(wordSpans);
        }
    } else {
        if (!targetWordSpan.classList.contains('incorrectWord')) {
            utils.applyIncorrectWordStyle(targetWordSpan);
            incrementError();
        }
    }
}

/**
 * Updates the innerHTML of the current word span to highlight typed characters.
 * @param {HTMLElement} wordSpan - The span element of the current word.
 * @param {number} typedLength - The number of characters typed (No-Tashkeel).
 */
function updateCurrentWordHighlighting(wordSpan, typedLength) {
    const originalText = wordSpan.dataset.originalText || wordSpan.textContent;
    
    if (typedLength === 0) {
        wordSpan.textContent = originalText;
        return;
    }

    // Calculate how many characters of the *displayed* text (with Tashkeel) 
    // correspond to the typed characters (without Tashkeel).
    const displayIndex = utils.getEndIndexInTashkeel(originalText, typedLength);

    const typedPart = originalText.substring(0, displayIndex);
    const remainingPart = originalText.substring(displayIndex);

    // Inject spans. Note: This might break ligatures visually in some browsers,
    // but it's the standard way to highlight partial text.
    wordSpan.innerHTML = `<span class="correct-char">${typedPart}</span>${remainingPart}`;
}

/**
 * Handles logic when a complete word is typed correctly, including word repetition.
 * @param {NodeListOf<HTMLSpanElement>} wordSpans - The list of word spans.
 */
function handleCorrectWord(wordSpans) {
    const correctWordSpan = wordSpans[mainQuranWordIndex];
    
    // Reset innerHTML to plain text before applying full word style to avoid nesting issues
    correctWordSpan.textContent = correctWordSpan.dataset.originalText || correctWordSpan.textContent;
    
    utils.applyCorrectWordStyle(correctWordSpan);
    correctWordSpan.classList.remove('cursor-active'); // Remove cursor from finished word

    inputElement.value = ""; // Clear input for the next repetition or word

    // --- Word Repetition Logic ---
    if (currentWordRepetition < wordRepeatCount) {
        // ** Repeat Current Word **
        currentWordRepetition++;
        // Optional: Add visual feedback for repetition count here if desired
        // Keep the same indices (mainQuranWordIndex, noTashkeelWordIndex)
        // The input is already cleared, ready for the next typing of the same word.
        correctWordSpan.classList.remove('correctWord'); // Temporarily remove style for re-typing
        correctWordSpan.classList.add('cursor-active'); // Add cursor back
        
        // Re-apply hidden style if hide button is active
        if (isHideAyahsButtonActive) {
            correctWordSpan.style.visibility = 'hidden';
        }

    } else {
        // ** Word Repetition Complete, Move On **
        currentWordRepetition = 1; // Reset counter for the *next* word

        // Check if the *next* span marks the end of an ayah BEFORE advancing index
        const isEndOfCurrentAyah = isNextWordAyahMarker(wordSpans, mainQuranWordIndex);

        if (isEndOfCurrentAyah) {
            // --- End of Ayah Reached ---
            if (currentAyahRepetition < ayahRepeatCount) {
                // ** Repeat Current Ayah **
                currentAyahRepetition++;
                showToast(`Repeating Ayah: ${utils.convertToArabicNumber(currentAyahRepetition)} / ${utils.convertToArabicNumber(ayahRepeatCount)}`);

                // Reset UI for the completed ayah (before resetting indices)
                resetCurrentAyahUI(mainQuranWordIndex);

                // Reset indices to the start of the *current* ayah
                mainQuranWordIndex = currentAyahStartIndex_Main;
                noTashkeelWordIndex = currentAyahStartIndex_NoTashkeel;

                // Recalculate scroll offsets based on the new first word of the ayah
                resetScrollOffsets(wordSpans, mainQuranWordIndex);

                // Ensure the first word of the repeated ayah is ready (remove correct style, set visibility)
                const firstWordSpan = wordSpans[mainQuranWordIndex];
                if (firstWordSpan) {
                    firstWordSpan.classList.remove('correctWord', 'incorrectWord');
                    firstWordSpan.classList.add('cursor-active'); // Add cursor
                    if (isHideAyahsButtonActive) {
                        firstWordSpan.style.visibility = 'hidden';
                    } else {
                        firstWordSpan.style.visibility = 'visible';
                    }
                }


            } else {
                // ** Ayah Repetition Complete, Move to Next Ayah **
                currentAyahRepetition = 1; // Reset ayah repetition counter for the *next* ayah
                handleNextWord(wordSpans); // Advance indices past the current word and the ayah marker
            }
        } else {
            // --- Move to Next Word (within the same ayah) ---
            handleNextWord(wordSpans); // Advance indices to the next word
        }
    }
}


/**
 * Advances the word indices and handles UI updates (scrolling, symbol skipping).
 * Checks if the end of the text has been reached.
 * @param {NodeListOf<HTMLSpanElement>} wordSpans - The list of word spans.
 */
function handleNextWord(wordSpans) {
    // Инкрементируем индексы для перехода к следующему слову/символу
    mainQuranWordIndex++;
    noTashkeelWordIndex++;
    currentLetterIndex = 0;

    // --- НАЧАЛО: Проверка на конец текста (сразу после инкремента) ---
    if (mainQuranWordIndex >= wordSpans.length) {
        // Мы обработали последнее слово/символ и вышли за пределы массива
        showToast("Surah Segment Complete!"); // Показываем сообщение о завершении
        if (timerInterval) {
            stopTimer();
            calculateAndDisplayResults();
        }
        inputElement.disabled = true; // Опционально: отключаем поле ввода
        console.log("End of text reached."); // Для отладки
        return; // Прекращаем дальнейшую обработку, так как текст закончился
    }
    // --- КОНЕЦ: Проверка на конец текста ---

    // Если не конец, продолжаем обработку: скроллинг и пропуск символов
    handleOffsetTop(wordSpans, wordSpans[mainQuranWordIndex]);
    handleSymbolSkip(wordSpans); // Пропускаем символы *после* основного инкремента индекса

    // --- НАЧАЛО: Повторная проверка на конец текста (после пропуска символов) ---
    // handleSymbolSkip мог увеличить mainQuranWordIndex до конца или за его пределы
    if (mainQuranWordIndex >= wordSpans.length) {
        // Мы обработали последний символ (который был пропущен) и вышли за пределы
        showToast("Surah Segment Complete!"); // Показываем сообщение о завершении
        if (timerInterval) {
            stopTimer();
            calculateAndDisplayResults();
        }
        inputElement.disabled = true; // Опционально: отключаем поле ввода
        console.log("End of text reached after skipping symbols."); // Для отладки
        return; // Прекращаем дальнейшую обработку
    }
    // --- КОНЕЦ: Повторная проверка на конец текста ---

    // Если текст еще не закончился, подготавливаем следующее слово к вводу
    const nextWordSpan = wordSpans[mainQuranWordIndex];
    if (nextWordSpan) {
        nextWordSpan.classList.add('cursor-active'); // Add cursor to next word
        
        if (isHideAyahsButtonActive && nextWordSpan.style.visibility !== 'hidden') {
            nextWordSpan.style.visibility = 'hidden'; // Скрываем следующее слово, если активна кнопка "Hide Ayahs"
        }
    }
}

/**
 * Checks if the word span at index + 1 is an ayah end marker `﴿`.
 * @param {NodeListOf<HTMLSpanElement>} wordSpans - Word spans.
 * @param {number} currentIndex - Index of the current word span.
 * @returns {boolean} True if the next span is an ayah marker.
 */
function isNextWordAyahMarker(wordSpans, currentIndex) {
    const nextIndex = currentIndex + 1;
    if (nextIndex < wordSpans.length) {
        // Check the content of the *next* span
        const nextWordText = wordSpans[nextIndex].textContent;
        return nextWordText.includes('﴿');
    }
    return false;
}

/**
 * Resets the visual styles for the words of the just-completed ayah.
 * @param {number} lastCorrectWordIndex - Index of the last word span of the ayah.
 */
function resetCurrentAyahUI(lastCorrectWordIndex) {
    const wordSpans = quranContainer.querySelectorAll('span');
    const ayahStartIndex = currentAyahStartIndex_Main;

    for (let i = ayahStartIndex; i <= lastCorrectWordIndex; i++) {
        const span = wordSpans[i];
        if (span) {
            span.classList.remove('correctWord', 'incorrectWord', 'cursor-active');

            // Reset visibility based on hide button state, but only if not hidden by scrolling
            span.style.display = ''
            if (isHideAyahsButtonActive) {
                span.style.visibility = 'hidden';
            } else {
                span.style.visibility = 'visible';
            }
        }
    }
    // Also reset the ayah marker span that follows
    const markerIndex = lastCorrectWordIndex + 1;
    if (markerIndex < wordSpans.length && wordSpans[markerIndex].textContent.includes('﴿')) {
        const markerSpan = wordSpans[markerIndex];
        markerSpan.classList.remove('correctWord', 'incorrectWord');
        if (markerSpan.style.display !== 'none') {
            if (isHideAyahsButtonActive) {
                markerSpan.style.visibility = 'hidden';
            } else {
                markerSpan.style.visibility = 'visible';
            }
        }
    }
}


/**
 * Recalculates scroll-related offsets when repeating an ayah.
 * @param {NodeListOf<HTMLSpanElement>} wordSpans - All word spans.
 * @param {number} currentWordIndex - Index of the word the user will type next.
 */
function resetScrollOffsets(wordSpans, currentWordIndex) {
    originalTopOffset = utils.getOriginalTopOffset(quranContainer);
    secondRowTopOffset = 0;
    refWord = null;

    if (currentWordIndex < wordSpans.length) {
        const startingSpan = wordSpans[currentWordIndex];
        refWord = startingSpan; // Start reference is the first word of the repeated ayah

        if (startingSpan.offsetTop > originalTopOffset) {
            originalTopOffset = startingSpan.offsetTop;
        }

        for (let i = currentWordIndex + 1; i < wordSpans.length; i++) {
            const span = wordSpans[i];
            if (span.offsetTop > originalTopOffset) {
                secondRowTopOffset = span.offsetTop;
                refWord = span;
                break;
            }
        }
        // If no second line is found within the ayah, refWord remains the starting span
    }
}

/**
 * Checks and skips Quran symbols, advancing the main index. Updates ayah start indices if marker skipped.
 * @param {NodeListOf<HTMLSpanElement>} wordSpans - Word spans.
 */
function handleSymbolSkip(wordSpans) {
    let skippedAyahMarker = false;

    // Пока текущий индекс в пределах массива И текст в текущем span является символом
    while (mainQuranWordIndex < wordSpans.length &&
        QURAN_SYMBOLS.some(char => wordSpans[mainQuranWordIndex].textContent.includes(char))) {
        const symbolSpan = wordSpans[mainQuranWordIndex];
        utils.applyCorrectWordStyle(symbolSpan); // Отмечаем символ как пройденный
        symbolSpan.classList.remove('cursor-active'); // Ensure no cursor on symbols

        // Проверяем, был ли пропущенный символ маркером аята
        if (symbolSpan.textContent.includes('﴿')) {
            skippedAyahMarker = true;
        }

        // Увеличиваем ТОЛЬКО основной индекс, пропуская символ
        mainQuranWordIndex++;

        // Важно: После пропуска символа, следующее слово может вызвать перенос строки
        // Проверяем это, ТОЛЬКО если мы все еще в пределах массива
        if (mainQuranWordIndex < wordSpans.length) {
            handleOffsetTop(wordSpans, wordSpans[mainQuranWordIndex]);
        } else {
            // Если после пропуска символа мы вышли за пределы, прерываем цикл
            // Завершение текста будет обработано в `handleNextWord` после вызова `handleSymbolSkip`
            break;
        }
    }

    // Если мы пропустили маркер аята и все еще в пределах массива,
    // обновляем стартовые индексы для следующего аята и сбрасываем счетчики повторений
    if (skippedAyahMarker && mainQuranWordIndex < wordSpans.length) {
        currentAyahStartIndex_Main = mainQuranWordIndex;
        // Синхронизируем индекс noTashkeel (он должен быть выровнен после инкремента в handleNextWord)
        currentAyahStartIndex_NoTashkeel = noTashkeelWordIndex;
        // Сбрасываем счетчик повторений аята, так как начинаем новый аят
        currentAyahRepetition = 1;
        // Сбрасываем счетчик повторений слова для первого слова нового аята
        currentWordRepetition = 1;
    }
    // Замечание: Явную проверку на конец текста внутри `handleSymbolSkip` делать не нужно,
    // так как `handleNextWord` выполнит эту проверку после вызова `handleSymbolSkip`.
}


/**
 * Detects line wrapping and handles hiding previous lines.
 * (Implementation based on logicOld.js behavior as requested)
 * Compares subsequent lines against the offset of the *original* second line.
 * @param {NodeListOf<HTMLSpanElement>} wordSpans - Word spans.
 * @param {HTMLSpanElement} wordToCheck - The current word span to check.
 */
function handleOffsetTop(wordSpans, wordToCheck) {
    // Защита: Убедимся, что есть слово для проверки и начальное смещение
    if (!wordToCheck || !originalTopOffset) return;

    // Получаем вертикальное смещение текущего слова
    const offsetTop = wordToCheck.offsetTop;

    // Проверяем, сместилось ли слово ниже первой строки
    if (offsetTop > originalTopOffset) {
        // Если secondRowTopOffset еще не установлен (т.е. это первый переход на вторую строку)
        if (secondRowTopOffset === 0) {
            // Запоминаем смещение второй строки
            secondRowTopOffset = offsetTop;
            // Устанавливаем refWord на первое слово этой второй строки
            refWord = wordToCheck;
        }

        // --- Начало логики из logicOld.js ---
        // Проверяем, сместилось ли слово ниже *запомненного* смещения второй строки
        // Это условие будет срабатывать при переходе на третью, четвертую и т.д. строки.
        // Важно: Используем здесь 'if', а не 'else if' (хотя функционально для этого случая разницы нет,
        // т.к. условия взаимоисключающие после первого срабатывания), чтобы точно соответствовать logicOld.
        // Ключевое отличие: secondRowTopOffset НЕ обновляется внутри этого блока.
        if (offsetTop > secondRowTopOffset) {
            // Если да, вызываем функцию для скрытия слов предыдущей строки (до refWord)
            utils.handleHiddenWords(wordSpans, refWord);
            // Обновляем refWord, чтобы он указывал на первое слово *новой* текущей строки
            refWord = wordToCheck;
            // secondRowTopOffset НЕ ОБНОВЛЯЕТСЯ здесь, как в logicOld.js
        }
        // --- Конец логики из logicOld.js ---
    }
}

// --- UI Interaction Handlers ---

/**
 * Toggles the visibility of untyped words and updates the button text.
 */
function handleHideAyahsButton() {
    isHideAyahsButtonActive = !isHideAyahsButtonActive;
    hideAyahsButton.textContent = isHideAyahsButtonActive ? "Show Ayahs" : "Hide Ayahs";
    applyHideAyahsVisibility(); // Apply the change to spans
}

/**
 * Applies the visibility style to word spans based on isHideAyahsButtonActive state.
 */
function applyHideAyahsVisibility() {
    const wordSpans = quranContainer.querySelectorAll('span');
    wordSpans.forEach(span => {
        // Only affect spans not hidden by scrolling ('display: none')
        if (span.style.display !== 'none') {
            // Hide if button active AND span is not already correctly typed
            if (isHideAyahsButtonActive && !span.classList.contains('correctWord')) {
                span.style.visibility = 'hidden';
            } else {
                // Show otherwise (unless it's an incorrect word during word repetition maybe?)\
                // Ensure symbols like ayah markers remain visible
                if (!QURAN_SYMBOLS.some(char => span.textContent.includes(char)) && span.classList.contains('incorrectWord')) {
                    // Keep incorrect words hidden if hiding is active? Decide on behavior.
                    // For simplicity, let's make them visible when Show is clicked.
                    span.style.visibility = 'visible';
                } else if (!span.textContent.includes(' ') || !QURAN_SYMBOLS.some(char => span.textContent.includes(char))) {
                    // Make normal words visible if not hiding
                    span.style.visibility = 'visible';
                }
                // Ensure symbols stay visible generally
                if (QURAN_SYMBOLS.some(char => span.textContent.includes(char))) {
                    span.style.visibility = 'visible';
                }
            }
        }
    });
}


/**
 * Processes the search query from the Surah selection input.
 * @param {string} query - The user's input query.
 */
function processSearch(query) {
    query = query.trim();

    if (query === "") {
        // Optionally reload default or do nothing. Let's reload default.
        if (currentSearchQuery !== "1:1") { // Avoid reloading if already at default
            getQuranSegment(SEGMENT_TYPE.SEARCH, "1:1", 'uthmani'); // Use SEARCH type
        }
        return;
    }

    const processedQuery = query.split(/[\s,:-]+/).filter(Boolean);
    let surahNum = NaN;
    let ayahNum = 1;

    if (processedQuery.length === 0 || processedQuery.length > 2) {
        showToast(`Invalid format. Use Surah:Ayah, Surah Ayah, or just Surah.`);
        return;
    }
    if (processedQuery.some(part => isNaN(part))) {
        showToast(`Please use numbers for Surah and Ayah.`);
        return;
    }

    surahNum = parseInt(processedQuery[0], 10);
    if (surahNum < 1 || surahNum > 114) {
        showToast(`Surah number must be between 1 and 114.`);
        return;
    }

    if (processedQuery.length === 2) {
        ayahNum = parseInt(processedQuery[1], 10);
        // Validation for ayahNum happens inside getQuranSegment now
    }

    // Use the query string "surahNum:ayahNum" as the ID for the search type
    const searchId = `${surahNum}:${ayahNum}`;
    currentSearchQuery = query; // Store the original user query if needed
    currentMode = 'search';
    // Fetch using the SEARCH type and the combined ID
    getQuranSegment(SEGMENT_TYPE.SURAH, searchId, 'uthmani');
}

/**
 * Displays a short notification message.
 * @param {string} message - The message to display.
 */
function showToast(message) {
    Toastify({
        text: message,
        duration: 3500,
        gravity: "bottom",
        position: 'center',
        close: true,
        style: {
            background: "linear-gradient(to right, #1473e6, #0D66D0)", // Match button color
            color: "#ffffff" // White text
        }
    }).showToast();
}

/**
 * Increments the total error count and updates the display.
 */
function incrementError() {
    totalErrors++;
    updateErrorDisplay();
}

/**
 * Updates the error count display element.
 */
function updateErrorDisplay() {
    if (errorCountDisplay) { // Check if element exists
        errorCountDisplay.textContent = totalErrors;
    }
}

// --- Timer Functions (Без изменений) ---
/**
 * Updates the timer display element with the current elapsed time (HH:MM:SS.ms).
 */
function updateTimerDisplay() {
    if (!startTime || !timerDisplayElement) return;
    const now = endTime ? endTime : Date.now();
    const elapsedMilliseconds = now - startTime;
    timerDisplayElement.textContent = utils.formatTime(elapsedMilliseconds);
}
/**
 * Starts the timer. Records the start time and sets a frequent interval for millisecond updates.
 */
function startTimer() {
    if (startTime !== null) return;
    if (timerInterval) clearInterval(timerInterval);
    startTime = Date.now();
    endTime = null;
    updateTimerDisplay();
    timerInterval = setInterval(updateTimerDisplay, 50);
}
/**
 * Stops the timer by clearing the interval.
 */
function stopTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
        endTime = Date.now();
        updateTimerDisplay(); // Final update for accuracy
    }
}
/**
 * Resets the timer: stops it, resets start time, and sets display to "00:00:00.000".
 */
function resetTimer() {
    stopTimer();
    startTime = null;
    endTime = null;
    if (timerDisplayElement) {
        timerDisplayElement.textContent = "00:00:00.000";
    }
}

// --- Table Population and Handling ---

/**
 * Populates the Surah selection table.
 */
function populateSurahSelectionTable() {
    if (!PROPERTIES_OF_SURAHS?.chapters || !surahSelectionTBody) {
        console.error("Surah data or table body not available for populating.");
        if (surahSelectionTBody) surahSelectionTBody.innerHTML = '<tr><td colspan="15">Failed to load Surah list.</td></tr>';
        return;
    }
    surahSelectionTBody.innerHTML = ''; // Clear previous rows
    const allResults = loadAllResults();

    PROPERTIES_OF_SURAHS.chapters.forEach(chapter => {
        const row = document.createElement('tr');
        row.dataset.segmentId = chapter.id; // Use generic dataset attribute

        row.innerHTML = `
            <td>${chapter.id}</td>
            <td style="font-family: 'IslamicFont', sans-serif;">${chapter.name_arabic}</td>
            <td>${chapter.name_simple}</td>
            <td>${chapter.revelation_place.charAt(0).toUpperCase() + chapter.revelation_place.slice(1)}</td>
            <td>${utils.convertToArabicNumber(chapter.verses_count)}</td>
        `;

        ['normal', 'blind'].forEach(mode => {
            // ИЗМЕНЕНО: Используем SEGMENT_TYPE.SURAH при получении результата
            const resultData = getResult(SEGMENT_TYPE.SURAH, chapter.id, mode);
            const displayTime = resultData?.time ?? '-';
            const displayErrors = resultData?.errors ?? '-';
            const displayScore = resultData?.score ?? '-';
            const displayRank = resultData?.rank ?? '-';

            row.innerHTML += `
                <td class="result-time-${mode}">${displayTime}</td>
                <td class="result-errors-${mode}">${displayErrors}</td>
                <td class="result-score-${mode}">${displayScore}</td>
                <td class="result-rank-${mode}">${displayRank}</td>
                <td class="has-text-centered">
                    <button class="button is-ghost start-segment-button" data-mode="${mode}">Start</button>
                </td>
            `;
        });
        surahSelectionTBody.appendChild(row);
    });

    // Add event listener using delegation
    surahSelectionTBody.addEventListener('click', handleStartSegment);
}


// ДОБАВЛЕНО: Функция для заполнения общих таблиц (Juz, Hizb, Rub, Page)
/**
 * Populates a generic selection table (Juz, Hizb, Rub', Page).
 * @param {string} type - The segment type (SEGMENT_TYPE constant).
 * @param {number} count - The total number of segments of this type.
 * @param {HTMLElement} tbodyElement - The tbody element of the table.
 * @param {string} labelPrefix - The label prefix (e.g., "Juz", "Hizb").
 */
function populateGenericSelectionTable(type, count, tbodyElement, labelPrefix) {
    if (!tbodyElement) {
        console.error(`Table body not found for type: ${type}`);
        return;
    }
    tbodyElement.innerHTML = ''; // Clear previous rows
    const allResults = loadAllResults();

    for (let i = 1; i <= count; i++) {
        const row = document.createElement('tr');
        row.dataset.segmentId = i; // Use generic dataset attribute

        row.innerHTML = `<td>${labelPrefix} ${i}</td>`; // Cell for the number/label

        ['normal', 'blind'].forEach(mode => {
            const resultData = getResult(type, i, mode); // Use type here
            const displayTime = resultData?.time ?? '-';
            const displayErrors = resultData?.errors ?? '-';
            const displayScore = resultData?.score ?? '-';
            const displayRank = resultData?.rank ?? '-';

            row.innerHTML += `
                <td class="result-time-${mode}">${displayTime}</td>
                <td class="result-errors-${mode}">${displayErrors}</td>
                <td class="result-score-${mode}">${displayScore}</td>
                <td class="result-rank-${mode}">${displayRank}</td>
                <td class="has-text-centered">
                    <button class="button is-ghost start-segment-button" data-mode="${mode}">Start</button>
                </td>
            `;
        });
        tbodyElement.appendChild(row);
    }
    // Add event listener using delegation
    tbodyElement.addEventListener('click', handleStartSegment);
}


// ИЗМЕНЕНО: Общий обработчик для всех кнопок Start
/**
 * Handles clicks on the "Start" buttons within any selection table.
 * @param {Event} event - The click event object.
 */
function handleStartSegment(event) {
    const clickedButton = event.target.closest('.start-segment-button');
    if (!clickedButton) return; // Click wasn't on a start button

    const clickedRow = clickedButton.closest('tr');
    const tbodyElement = clickedRow?.parentElement; // Get the parent tbody
    if (!tbodyElement || !clickedRow?.dataset.segmentId) {
        console.error("Could not find row, tbody, or segment ID for clicked button.");
        return; // Failed to find row or segment ID
    }

    const selectedSegmentId = clickedRow.dataset.segmentId; // Get ID from row
    const selectedMode = clickedButton.dataset.mode; // Get mode from button

    // Determine the type based on the tbody's ID
    let selectedType;
    switch (tbodyElement.id) {
        case 'surah-selection-tbody': selectedType = SEGMENT_TYPE.SURAH; break;
        case 'juz-selection-tbody': selectedType = SEGMENT_TYPE.JUZ; break;
        case 'hizb-selection-tbody': selectedType = SEGMENT_TYPE.HIZB; break;
        case 'rub-selection-tbody': selectedType = SEGMENT_TYPE.RUB; break;
        case 'page-selection-tbody': selectedType = SEGMENT_TYPE.PAGE; break;
        default:
            console.error("Unknown tbody ID:", tbodyElement.id);
            return;
    }


    if (selectedSegmentId && selectedMode && selectedType) {
        // Save the selected parameters (type is already set by switch)
        currentSelectionId = selectedSegmentId; // Save the ID (might be number or string for surah)
        currentMode = selectedMode;     // Save selected mode

        // Hide selection table view
        if (surahSelectionSection) surahSelectionSection.classList.add('is-hidden');
        // Show main typing interface
        if (mainTypingSection) mainTypingSection.classList.remove('is-hidden');

        // Load the selected segment
        getQuranSegment(selectedType, selectedSegmentId, 'uthmani');

        // Apply mode-specific UI settings immediately
        applyModeSettings();

    } else {
        console.error("Missing data for starting segment:", { selectedSegmentId, selectedMode, selectedType });
    }
}


// --- View Toggling ---

/**
 * Toggles visibility between the main typing interface and the selection table view.
 */
function toggleSurahSelectionView() {
    if (!mainTypingSection || !surahSelectionSection) return;

    const isTypingVisible = !mainTypingSection.classList.contains('is-hidden');

    if (isTypingVisible) {
        // --- Switching FROM typing TO selection view ---
        mainTypingSection.classList.add('is-hidden');
        surahSelectionSection.classList.remove('is-hidden');
        stopTimer(); // Stop timer if running
        // Clear search input and typing input when switching TO selection
        const surahInputElement = document.getElementById("Surah-selection-input");
        if (surahInputElement) surahInputElement.value = '';
        if (inputElement) {
            inputElement.value = ''; // Clear typing field
            inputElement.classList.remove('incorrectWord');
        }
        // ДОБАВЛЕНО: Опционально, обновляем данные таблиц при показе
        // Это полезно, если результаты могли измениться во время печати
        // Но может быть медленно, если таблицы большие. Пока не будем обновлять.
        // populateAllSelectionTables(); // Раскомментировать для обновления при каждом показе
    } else {
        // --- Switching FROM selection view TO typing ---
        surahSelectionSection.classList.add('is-hidden');
        mainTypingSection.classList.remove('is-hidden');

        applyModeSettings(); // Ensure Hide Ayahs button state is correct

        // Enable and focus input if content is already loaded
        if (inputElement && quranContainer.hasChildNodes()) {
            inputElement.disabled = false;
            inputElement.focus();
        } else if (!quranContainer.hasChildNodes()) {
            // If no content (e.g., initial load error), load default
            getQuranSegment(SEGMENT_TYPE.SURAH, "1:1", 'uthmani'); // Load default Surah
        }
    }
}

// --- Results Calculation and Storage ---

/**
 * Calculates and displays the final results (CPM, Score, Rank)
 */
function calculateAndDisplayResults() {
    // Check if timer actually ran and segment has characters
    if (!startTime || !endTime || totalCharsInSegment <= 0) {
        console.warn("Cannot calculate results: Timer not run or no characters.", { startTime, endTime, totalCharsInSegment });
        resetResultsDisplay();
        // Don't save results if they can't be calculated
        return;
    }

    const elapsedMilliseconds = endTime - startTime;
    const numberOfErrors = totalErrors;
    const numberOfChars = totalCharsInSegment;

    // 1. Base metrics
    const cpm = utils.calculateCPM(numberOfChars, elapsedMilliseconds);
    const errorRate = utils.calculateErrorRate(numberOfErrors, numberOfChars);
    const adjustedCPM = utils.calculateAdjustedCPM(cpm, numberOfErrors);

    // 2. Final score
    const score = utils.calculateScore(adjustedCPM, TARGET_CPM);

    // 3. Rank
    const rank = utils.determineRank(score, errorRate);

    // 4. Display results
    if (acpmDisplay) acpmDisplay.textContent = Math.round(adjustedCPM);
    if (scoreDisplay) scoreDisplay.textContent = `${score}%`;
    if (rankDisplay) rankDisplay.textContent = rank;

    // --- Save Result ---
    // Only save if the segment was started from a selection table (not search)
    // AND if we have a valid type and ID
    if (currentSelectionType !== SEGMENT_TYPE.SEARCH && currentSelectionId !== null) {
        const formattedTime = utils.formatTime(elapsedMilliseconds);
        const resultData = {
            score: score,
            time: formattedTime,
            errors: numberOfErrors,
            rank: rank
        };
        saveResult(currentSelectionType, currentSelectionId, currentMode, resultData);
    } else {
        console.log("Result not saved (Search mode or invalid ID/Type)");
    }
    console.log(`Results - Type: ${currentSelectionType}, ID: ${currentSelectionId}, Mode: ${currentMode} | Time: ${utils.formatTime(elapsedMilliseconds)}, Errors: ${numberOfErrors}, Chars: ${numberOfChars}, CPM: ${cpm.toFixed(0)}, aCPM: ${adjustedCPM.toFixed(0)}, Score: ${score}, Rank: ${rank}`); // Debugging
}


/**
 * Resets the result display elements to their initial state.
 */
function resetResultsDisplay() {
    if (acpmDisplay) acpmDisplay.textContent = "-";
    if (scoreDisplay) scoreDisplay.textContent = "-";
    if (rankDisplay) rankDisplay.textContent = "-";
}

// ИЗМЕНЕНО: Функции работы с Local Storage для поддержки типов
/**
 * Loads all saved results from Local Storage.
 * @returns {object} Object with results like { type: { id: { mode: result } } } or empty object.
 */
function loadAllResults() {
    try {
        const storedResults = localStorage.getItem(RESULTS_STORAGE_KEY);
        // Basic validation: check if it's parseable JSON
        if (storedResults) {
            const parsed = JSON.parse(storedResults);
            // Add a check to ensure it's an object (basic structure check)
            if (typeof parsed === 'object' && parsed !== null) {
                return parsed;
            } else {
                console.warn("Stored results format is invalid, returning empty object.");
                localStorage.removeItem(RESULTS_STORAGE_KEY); // Clear invalid data
                return {};
            }
        }
        return {};
    } catch (error) {
        console.error("Error loading results from Local Storage:", error);
        // Attempt to clear potentially corrupted data
        localStorage.removeItem(RESULTS_STORAGE_KEY);
        return {}; // Return empty object on error
    }
}

/**
 * Gets saved result for a specific segment type, ID, and mode.
 * @param {string} type Segment type (SEGMENT_TYPE constant).
 * @param {number|string} id Segment ID.
 * @param {'normal'|'blind'} mode Mode.
 * @returns {object | null} Result object { score, time, errors, rank } or null.
 */
function getResult(type, id, mode) {
    const allResults = loadAllResults();
    // Check if type exists, then id, then mode
    return allResults?.[type]?.[id]?.[mode] || null;
}

/**
 * Saves result for a specific segment type, ID, and mode to Local Storage.
 * Only saves if the new score is better than the existing one.
 * @param {string} type Segment type (SEGMENT_TYPE constant).
 * @param {number|string} id Segment ID.
 * @param {'normal'|'blind'} mode Mode.
 * @param {object} resultData Result object { score, time, errors, rank }.
 */
function saveResult(type, id, mode, resultData) {
    // Basic validation
    if (!type || id === null || id === undefined || !mode || !resultData || typeof resultData.score !== 'number') {
        console.error("Cannot save result: Invalid data provided.", { type, id, mode, resultData });
        return;
    }

    const allResults = loadAllResults();

    // Ensure structure exists
    if (!allResults[type]) {
        allResults[type] = {};
    }
    if (!allResults[type][id]) {
        allResults[type][id] = {};
    }

    const existingResult = allResults[type][id]?.[mode];
    let shouldSave = true; // Assume we should save by default

    if (existingResult && typeof existingResult.score === 'number') {
        // Compare scores only if existing score is a valid number
        if (resultData.score <= existingResult.score) {
            console.log(`Result for ${type} ${id} (${mode}) not saved (Score ${resultData.score} is not better than ${existingResult.score})`);
            shouldSave = false; // Don't save if score isn't better
        }
    }

    if (shouldSave) {
        allResults[type][id][mode] = resultData; // Save or overwrite result
        if (!existingResult || resultData.score > (existingResult?.score ?? -1)) {
            showToast("New Record!"); // Show only if it's a new record or better score
        }


        try {
            localStorage.setItem(RESULTS_STORAGE_KEY, JSON.stringify(allResults));
            console.log(`Result saved for ${type} ${id} (${mode}):`, resultData);
            // Update the display in the corresponding table immediately
            updateSegmentTableResultDisplay(type, id, mode, resultData);
        } catch (error) {
            console.error("Error saving results to Local Storage:", error);
            showToast("Could not save your result.");
        }
    }
}


// ИЗМЕНЕНО: Обновление отображения результата в таблице
/**
 * Updates the result display (Time, Errors, Score, Rank) in the specific selection table row.
 * @param {string} type Segment type (SEGMENT_TYPE constant).
 * @param {number|string} id Segment ID.
 * @param {'normal'|'blind'} mode Mode.
 * @param {object} resultData New result object { score, time, errors, rank }.
 */
function updateSegmentTableResultDisplay(type, id, mode, resultData) {
    let tbodyElement;
    // Find the correct tbody based on type
    switch (type) {
        case SEGMENT_TYPE.SURAH: tbodyElement = surahSelectionTBody; break;
        case SEGMENT_TYPE.JUZ: tbodyElement = juzSelectionTBody; break;
        case SEGMENT_TYPE.HIZB: tbodyElement = hizbSelectionTBody; break;
        case SEGMENT_TYPE.RUB: tbodyElement = rubSelectionTBody; break;
        case SEGMENT_TYPE.PAGE: tbodyElement = pageSelectionTBody; break;
        default: return; // Unknown type
    }

    if (!tbodyElement || !resultData) return;

    // Find the row using the data-segment-id attribute
    const row = tbodyElement.querySelector(`tr[data-segment-id="${id}"]`);
    if (!row) {
        console.warn(`Row not found in table for ${type} ${id}`);
        return;
    }

    // Find cells by class within the row
    const timeCell = row.querySelector(`.result-time-${mode}`);
    const errorsCell = row.querySelector(`.result-errors-${mode}`);
    const scoreCell = row.querySelector(`.result-score-${mode}`);
    const rankCell = row.querySelector(`.result-rank-${mode}`);

    // Format data for display (handle null/undefined)
    const displayTime = resultData.time ?? '-';
    const displayErrors = resultData.errors ?? '-';
    const displayScore = resultData.score ?? '-';
    const displayRank = resultData.rank ?? '-';

    // Update cell content
    if (timeCell) timeCell.textContent = displayTime;
    if (errorsCell) errorsCell.textContent = displayErrors;
    if (scoreCell) scoreCell.textContent = displayScore;
    if (rankCell) rankCell.textContent = displayRank;
}

// --- Tab Switching Logic --- ДОБАВЛЕНО
/**
 * Handles clicks on the tab links.
 * @param {Event} event - The click event.
 */
function handleTabClick(event) {
    const clickedTab = event.currentTarget; // The <li> element
    const targetTabName = clickedTab.dataset.tab;

    if (!targetTabName || clickedTab.classList.contains('is-active')) {
        return; // Do nothing if clicking the active tab or invalid tab
    }

    // Remove 'is-active' from all tabs and hide all content
    tabLinks.forEach(link => link.classList.remove('is-active'));
    tabContentContainers.forEach(container => container.classList.add('is-hidden'));

    // Activate the clicked tab
    clickedTab.classList.add('is-active');

    // Show the corresponding content
    const targetContent = document.getElementById(`tab-content-${targetTabName}`);
    if (targetContent) {
        targetContent.classList.remove('is-hidden');
    } else {
        console.error(`Tab content not found for: tab-content-${targetTabName}`);
    }
}

/**
 * Handles keydown events globally, specifically looking for the Escape key to restart.
 * @param {KeyboardEvent} event The keyboard event object.
 */
function handleRestartKey(event) {
    // Check if the pressed key is Escape
    if (event.key === 'Escape') {
        // Check if the main typing section is currently visible
        // and if we have a valid segment selected (type and ID are not null)
        if (mainTypingSection && !mainTypingSection.classList.contains('is-hidden') &&
            currentSelectionType !== null && currentSelectionId !== null) {
            // Prevent default Escape behavior (like closing modals, if any were present)
            event.preventDefault();

            // Show a confirmation toast
            // showToast(`Restarting ${currentSelectionType} ${currentSelectionId}`);

            // Call getQuranSegment with the currently selected type and ID to restart
            // The getQuranSegment function already handles resetting state.
            // We keep the current script ('uthmani') and current mode.
            getQuranSegment(currentSelectionType, currentSelectionId, 'uthmani');
        }
    }
}

// --- Event Listeners Setup ---

/**
 * Adds all necessary event listeners to the UI elements.
 */
function addListeners() {
    // Dark Mode Toggle
    document.getElementById('dark-mode-toggle').addEventListener('click', () => {
        isDarkMode = utils.toggleDarkMode(isDarkMode);
    });

    // Hide Ayahs Button (only works in normal/search mode)
    hideAyahsButton.addEventListener('click', handleHideAyahsButton);

    // Main Input Field
    inputElement.addEventListener("input", handleInput);
    inputElement.addEventListener("focus", () => { // Clear potential error style on focus
        const wordSpans = quranContainer.querySelectorAll('span');
        if (mainQuranWordIndex < wordSpans.length) {
            const currentSpan = wordSpans[mainQuranWordIndex];
            if (currentSpan) { // Check if span exists
                currentSpan.classList.remove('incorrectWord');
            }
        }
    });
    
    // Global click listener to maintain focus on the hidden input
    document.addEventListener('click', (event) => {
        // Only focus if typing section is visible and we aren't clicking on another input/button
        if (mainTypingSection && !mainTypingSection.classList.contains('is-hidden')) {
            const isControl = event.target.closest('input, button, a');
            if (!isControl && inputElement) {
                inputElement.focus();
            }
        }
    });

    // Ayah Repetition Input
    repeatCountInput.addEventListener('change', (event) => {
        const newCount = parseInt(event.target.value, 10);
        ayahRepeatCount = (!isNaN(newCount) && newCount >= 1) ? newCount : 1;
        event.target.value = ayahRepeatCount; // Update input field
        if (ayahRepeatCount !== newCount) showToast("Ayah repetition count must be 1 or greater.");
    });
    repeatCountInput.addEventListener('input', (event) => { // Allow only numbers
        event.target.value = event.target.value.replace(/[^0-9]/g, '');
    });

    // Word Repetition Input
    wordRepeatCountInput.addEventListener('change', (event) => {
        const newCount = parseInt(event.target.value, 10);
        wordRepeatCount = (!isNaN(newCount) && newCount >= 1) ? newCount : 1;
        event.target.value = wordRepeatCount; // Update input field
        if (wordRepeatCount !== newCount) showToast("Word repetition count must be 1 or greater.");
    });
    wordRepeatCountInput.addEventListener('input', (event) => { // Allow only numbers
        event.target.value = event.target.value.replace(/[^0-9]/g, '');
    });


    // Surah Selection Input and Button (Top Search Bar)
    const surahInputElement = document.getElementById("Surah-selection-input");
    const surahProcessButton = document.getElementById("Display-Surah-button");

    surahProcessButton.addEventListener("click", () => {
        processSearch(surahInputElement.value); // This now calls getQuranSegment with type SEARCH
    });
    surahInputElement.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
            processSearch(surahInputElement.value); // This now calls getQuranSegment with type SEARCH
        }
    });

    // Toggle Selection View Button
    if (changeSurahButton) {
        changeSurahButton.addEventListener('click', toggleSurahSelectionView);
    }

    // --- ДОБАВЛЕНО: Tab Link Listeners ---
    if (tabLinks) {
        tabLinks.forEach(link => {
            link.addEventListener('click', handleTabClick);
        });
    }

    // --- ИЗМЕНЕНО: Start Button listeners are now added dynamically in population functions ---
    // The handleStartSegment function handles events via delegation.

    // Auto-focus on the main input field when the page loads (if typing section is visible)
    document.addEventListener("DOMContentLoaded", () => {
        if (!mainTypingSection.classList.contains('is-hidden') && inputElement) {
            inputElement.focus();
        }
    });

    // Global listener for the Escape key to restart the current segment
    document.addEventListener('keydown', handleRestartKey);
}

// --- Application Entry Point ---

// ДОБАВЛЕНО: Функция для вызова всех функций заполнения таблиц
function populateAllSelectionTables() {
    populateSurahSelectionTable();
    populateGenericSelectionTable(SEGMENT_TYPE.JUZ, COUNT.JUZ, juzSelectionTBody, "Juz");
    populateGenericSelectionTable(SEGMENT_TYPE.HIZB, COUNT.HIZB, hizbSelectionTBody, "Hizb");
    populateGenericSelectionTable(SEGMENT_TYPE.RUB, COUNT.RUB, rubSelectionTBody, "Rub'");
    populateGenericSelectionTable(SEGMENT_TYPE.PAGE, COUNT.PAGE, pageSelectionTBody, "Page");
}

/**
 * Initializes the application.
 */
function runApp() {
    cacheDOMElements();
    utils.initDarkMode(isDarkMode);
    addListeners();
    resetResultsDisplay(); // Reset footer display

    setupSurahData()
        .then(() => {
            // Populate selection tables in the background (they are initially hidden)
            populateAllSelectionTables();

            // Ensure typing section is visible and selection section is hidden initially
            if (mainTypingSection) mainTypingSection.classList.remove('is-hidden');
            if (surahSelectionSection) surahSelectionSection.classList.add('is-hidden');

            // Load the default Surah 1, Ayah 1 for the typing view
            // Set initial state before loading
            currentSelectionType = SEGMENT_TYPE.SURAH; // Default type
            currentSelectionId = 1; // Default ID
            currentMode = 'normal'; // Default mode
            currentSearchQuery = "1:1";
            getQuranSegment(SEGMENT_TYPE.SURAH, 1, 'uthmani'); // Load Surah 1

        })
        .catch(error => {
            console.error('Error during application initialization:', error);
            showToast("Failed to initialize application data. Please refresh.");
            resetResultsDisplay();
            // Show error message in the main typing area
            if (mainTypingSection) mainTypingSection.classList.remove('is-hidden');
            if (quranContainer) quranContainer.innerHTML = '<p class="has-text-danger has-text-centered">Error loading data. Try refreshing the page.</p>';
            if (surahSelectionSection) surahSelectionSection.classList.add('is-hidden');
            if (errorCountDisplay) errorCountDisplay.textContent = "Error";
            if (inputElement) inputElement.disabled = true;
            if (acpmDisplay) acpmDisplay.textContent = "Error";
            if (scoreDisplay) scoreDisplay.textContent = "Error";
            if (rankDisplay) rankDisplay.textContent = "Error";
        });
}

// Run the application
runApp();
```

### 4. index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Explore the beauty of the Quran and enhance your Arabic skills on Quran Type! Type and explore Quranic text to improve your Arabic writing, reading, and vocabulary. Unlock the beauty of the language while deepening your understanding of the sacred Quran.">
    <title>Quran Type +</title>

    <!-- Bulma CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bulma@1.0.0/css/bulma.min.css">
    <!-- Пользовательские стили поверх Bulma -->
    <link rel="stylesheet" href="src/css/styles.css">

    <!-- Toastify -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/toastify-js/src/toastify.min.css">
    <script src="https://cdn.jsdelivr.net/npm/toastify-js"></script>

    <!-- Пользовательские скрипты -->
    <script type="module" src="src/js/logic.js" defer></script>

    <!-- Шрифты -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Noto+Naskh+Arabic&display=swap" rel="stylesheet">

    <!-- Favicons -->
    <link rel="apple-touch-icon" sizes="180x180" href="public/icons/apple-touch-icon.png">
    <link rel="icon" type="image/png" sizes="32x32" href="public/icons/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="public/icons/favicon-16x16.png">
    <link rel="mask-icon" href="public/icons/safari-pinned-tab.svg" color="#5bbad5">
    <link rel="shortcut icon" href="public/icons/favicon.ico">
    <meta name="msapplication-TileColor" content="#da532c">
    <meta name="msapplication-config" content="public/icons/browserconfig.xml">
    <meta name="theme-color" content="#ffffff">

</head>
<body>
    <section class="section pt-4 pb-4">
        <nav class="level">
            <!-- Left side -->
            <div class="level-left">
                <div class="level-item">
                    <h1 class="title logo-title">Quran Type +</h1>
                </div>
            </div>

            <!-- Right side -->
            <div class="level-right">
                <div class="level-item">
                    <!-- Search -->
                    <div class="field has-addons">
                        <div class="control">
                            <label for='Surah-selection-input' class="is-sr-only">Enter Surah and Verse:</label>
                            <input class="input" type="search" placeholder="Enter Surah:Ayah" aria-label="Search Quran"
                                   autocomplete="off" id="Surah-selection-input">
                        </div>
                        <div class="control">
                            <button class="button is-primary" id="Display-Surah-button">
                                Display
                            </button>
                        </div>
                    </div>
                </div>
                <div class="level-item">
                    <!-- Theme Toggle (оставляем только изображения внутри кнопки) -->
                   <button class="button is-text image-button mr-2" id="dark-mode-toggle" aria-label="Toggle theme" title="Сменить тему"> <!-- Добавляем is-text, image-button, title -->
                       <img src="public/images/LanternLight.svg" alt="Light Mode" id="light-mode-icon" class="theme-icon button-icon">
                       <img src="public/images/LanternDark.svg" alt="Dark Mode" id="dark-mode-icon" class="theme-icon button-icon" style="display: none;">
                   </button>
                    <!-- Кнопка Изменить Суру -->
                    <button class="button is-text image-button" id="change-surah-button" aria-label="Изменить Суру" title="Изменить Суру">
                        <img src="public/images/MenuLight.svg" alt="Menu" id="light-menu-icon" class="button-icon">
                        <img src="public/images/MenuDark.svg" alt="Menu" id="dark-menu-icon" class="theme-icon button-icon">
                    </button>
                </div>
            </div>
        </nav>
    </section>

    <!-- ИЗМЕНЕНО: Добавлены data-tab атрибуты и начальное состояние -->
    <section class="section pt-4 pb-4 is-hidden" id="surah-selection-section">
        <div class="container">
            <div class="tabs is-centered is-boxed">
                <ul>
                    <li class="is-active" data-tab="surah"><a>Surah</a></li>
                    <li data-tab="juz"><a>Juz</a></li>
                    <li data-tab="hizb"><a>Hizb</a></li>
                    <li data-tab="rub"><a>Rub'</a></li>
                    <li data-tab="page"><a>Page</a></li>
                </ul>
            </div>
            <!-- ИЗМЕНЕНО: Добавлен класс .tab-content для всех контейнеров -->
            <div id="tab-content-surah" class="tab-content">
                <!-- СУЩЕСТВУЮЩИЙ КОНТЕЙНЕР ТАБЛИЦЫ СУР -->
                <div class="table-container">
                    <table class="table is-bordered selection-table is-striped is-narrow is-hoverable is-fullwidth" id="surah-selection-table"> <!-- ДОБАВЛЕНО: selection-table class -->
                        <thead>
                            <tr>
                              <th rowspan="2">№</th>
                              <th rowspan="2">سورة</th>
                              <th rowspan="2">Surah</th>
                              <th rowspan="2">Period</th>
                              <th rowspan="2">Ayah</th>
                              <th colspan="5">Normal Mode</th>
                              <th colspan="5">Blind Mode</th>
                            </tr>
                            <tr>
                              <th>Time</th><th>Missclicks</th><th>Score</th><th>Rank</th><th></th> <!-- Normal -->
                              <th>Time</th><th>Missclicks</th><th>Score</th><th>Rank</th><th></th> <!-- Blind -->
                            </tr>
                        </thead>
                        <tbody id="surah-selection-tbody">
                            <!-- Строки для Сур будут добавлены динамически -->
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- ИЗМЕНЕНО: Добавлен is-hidden и класс .tab-content, класс .selection-table -->
            <div id="tab-content-juz" class="tab-content is-hidden">
                <div class="table-container">
                    <table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth selection-table" id="juz-selection-table"> <!-- ДОБАВЛЕНО: selection-table class -->
                        <thead>
                            <tr>
                                <th rowspan="2">Juz №</th>
                                <th colspan="5">Normal Mode</th>
                                <th colspan="5">Blind Mode</th>
                              </tr>
                              <tr>
                                <th>Time</th><th>Missclicks</th><th>Score</th><th>Rank</th><th></th> <!-- Normal -->
                                <th>Time</th><th>Missclicks</th><th>Score</th><th>Rank</th><th></th> <!-- Blind -->
                              </tr>
                        </thead>
                        <tbody id="juz-selection-tbody">
                             <!-- Строки для Джузов будут добавлены динамически -->
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- ИЗМЕНЕНО: Добавлен is-hidden и класс .tab-content, класс .selection-table -->
            <div id="tab-content-hizb" class="tab-content is-hidden">
                <div class="table-container">
                     <table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth selection-table" id="hizb-selection-table"> <!-- ДОБАВЛЕНО: selection-table class -->
                        <thead>
                            <tr>
                                <th rowspan="2">Hizb №</th>
                                <th colspan="5">Normal Mode</th>
                                <th colspan="5">Blind Mode</th>
                              </tr>
                              <tr>
                                <th>Time</th><th>Missclicks</th><th>Score</th><th>Rank</th><th></th> <!-- Normal -->
                                <th>Time</th><th>Missclicks</th><th>Score</th><th>Rank</th><th></th> <!-- Blind -->
                              </tr>
                        </thead>
                        <tbody id="hizb-selection-tbody">
                            <!-- Строки для Хизбов будут добавлены динамически -->
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- ИЗМЕНЕНО: Добавлен is-hidden и класс .tab-content, класс .selection-table -->
            <div id="tab-content-rub" class="tab-content is-hidden">
                 <div class="table-container">
                     <table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth selection-table" id="rub-selection-table"> <!-- ДОБАВЛЕНО: selection-table class -->
                        <thead>
                             <tr>
                                <th rowspan="2">Rub' №</th>
                                <th colspan="5">Normal Mode</th>
                                <th colspan="5">Blind Mode</th>
                              </tr>
                              <tr>
                                <th>Time</th><th>Missclicks</th><th>Score</th><th>Rank</th><th></th> <!-- Normal -->
                                <th>Time</th><th>Missclicks</th><th>Score</th><th>Rank</th><th></th> <!-- Blind -->
                              </tr>
                        </thead>
                        <tbody id="rub-selection-tbody">
                             <!-- Строки для Руб аль Хизб будут добавлены динамически -->
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- ИЗМЕНЕНО: Добавлен is-hidden и класс .tab-content, класс .selection-table -->
             <div id="tab-content-page" class="tab-content is-hidden">
                 <div class="table-container">
                    <table class="table is-bordered is-striped is-narrow is-hoverable is-fullwidth selection-table" id="page-selection-table"> <!-- ДОБАВЛЕНО: selection-table class -->
                         <thead>
                            <tr>
                                <th rowspan="2">Page №</th>
                                <th colspan="5">Normal Mode</th>
                                <th colspan="5">Blind Mode</th>
                              </tr>
                              <tr>
                                <th>Time</th><th>Missclicks</th><th>Score</th><th>Rank</th><th></th> <!-- Normal -->
                                <th>Time</th><th>Missclicks</th><th>Score</th><th>Rank</th><th></th> <!-- Blind -->
                              </tr>
                        </thead>
                        <tbody id="page-selection-tbody">
                            <!-- Строки для Страниц будут добавлены динамически -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </section>

    <!-- Оберните существующий основной контент в этот div -->
    <div id="main-typing-section">

    <section class="section pt-2 pb-5">
        <div class="container has-text-centered">
            <!-- Surah Details -->
            <div id="Surah-details" class="mb-4">
                <div id="Surah-name" class="subtitle is-4"></div>
                <div id="Basmallah" class="is-size-5"></div>
            </div>

            <!-- Quran Text Container -->
            <div id="Quran-container" class="content has-text-right mb-5" dir="rtl">
                <!-- Spans will be injected here by JS -->
            </div>
            <!-- Hidden Container for No-Tashkeel text -->
            <div id="noTashkeelContainer" style="display: none;"></div>

            <!-- Input and Controls Container -->
            <div id="Quran-input-controls-container" class="is-flex is-flex-direction-column is-align-items-center">
                 <!-- Input Row -->
                <div class="field is-grouped is-grouped-centered is-fullwidth mb-4" id="Quran-input-container">
                    <div class="control">
                        <button id="hideAyahsButton" class="button is-primary is-medium">Hide Ayahs</button>
                    </div>
                    <div class="control">
                        <label for='inputField' class="is-sr-only">Type the verses from the Quran shown:</label>
                        <!-- ИЗМЕНЕНО: Input теперь скрыт стилями, но остается в DOM -->
                        <input class="input is-medium" autocomplete="off" id="inputField" dir="rtl">
                    </div>
                </div>

                <!-- Repetition Controls Row -->
                <div id="repetitionControlsRow" class="field is-grouped is-grouped-centered is-grouped-multiline" dir="ltr"> <!-- Force LTR for controls -->
                    <!-- Ayah Repetition -->
                    <div class="control">
                        <div class="field has-addons" id="wordRepetitionContainer">
                            <div class="tags has-addons">
                                <span class="tag">Repeat Ayah:</span>
                                <input type="number" id="repeatCountInput" name="repeatCount" min="1" value="1" class="input is-small repetition-input">
                                <span class="tag">times</span>
                            </div>
                        </div>
                    </div>
                    <!-- Word Repetition -->
                    <div class="control">
                        <div class="field has-addons" id="wordRepetitionContainer">
                            <div class="tags has-addons">
                                <span class="tag">Repeat Word:</span>
                                <input type="number" id="wordRepeatCountInput" name="wordRepeatCount" min="1" value="1" class="input is-small repetition-input">
                                <span class="tag">times</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</div>

    <footer class="footer pt-5 pb-5">
        <div class="content has-text-centered">
            <div class="level">
                 <!-- Error Counter -->
                <div class="level-item has-text-centered">
                    <div id="errorCounterContainer">
                        <span id="errorCountLabel" class="has-text-weight-bold">Errors: </span>
                        <span id="errorCountDisplay" class="has-text-weight-bold">0</span>
                    </div>
                </div>
                <!-- Timer -->
                <div class="level-item has-text-centered">
                    <div id="timerContainer">
                        <span id="timerLabel" class="has-text-weight-bold">Time: </span>
                        <span id="timerDisplay" class="has-text-weight-bold">00:00:00.000</span>
                    </div>
                </div>
                <!-- ДОБАВЛЕНО: Adjusted CPM -->
                <div class="level-item has-text-centered">
                    <div id="acpmContainer">
                        <span id="acpmLabel" class="has-text-weight-bold">aCPM: </span>
                        <span id="acpmDisplay" class="has-text-weight-bold">-</span>
                    </div>
                </div>
                <!-- ДОБАВЛЕНО: Score -->
                <div class="level-item has-text-centered">
                    <div id="scoreContainer">
                        <span id="scoreLabel" class="has-text-weight-bold">Score: </span>
                        <span id="scoreDisplay" class="has-text-weight-bold">-</span>
                    </div>
                </div>
                <!-- ДОБАВЛЕНО: Rank -->
                <div class="level-item has-text-centered">
                    <div id="rankContainer">
                        <span id="rankLabel" class="has-text-weight-bold">Rank: </span>
                        <span id="rankDisplay" class="has-text-weight-bold">-</span>
                    </div>
                </div>
                 <!-- Links -->
                 <div class="level-item has-text-centered">
                    <a href="https://api-docs.quran.com/docs/category/quran.com-api" target="_blank" class="footer-link">Quran Api source</a>
                 </div>
                 <div class="level-item has-text-centered">
                     <a href="https://qurantype.com" target="_blank" class="footer-link">Original Website</a>
                 </div>
            </div>
        </div>
    </footer>
</body>
</html>
```