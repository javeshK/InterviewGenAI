/*
==========================================================
InterviewGen AI
static/js/interview.js

Handles:
✓ Timer
✓ Submit Answer
✓ Loading Animation
✓ Question Updates
✓ Score Updates
✓ Progress Updates
✓ Interview Completion

Part 1
==========================================================
*/

"use strict";

// ======================================================
// DOM ELEMENTS
// ======================================================

const interviewId = document.getElementById("sessionId").value;

const questionElement =
    document.getElementById("currentQuestion");

const answerBox =
    document.getElementById("answerBox");

const submitButton =
    document.getElementById("submitAnswer");

const finishButton =
    document.getElementById("finishInterview");

const clearButton =
    document.getElementById("clearAnswer");

const thinkingCard =
    document.getElementById("thinkingCard");

const aiStatus =
    document.getElementById("aiStatus");

const feedbackCard =
    document.getElementById("feedbackCard");

const progressBar =
    document.getElementById("progressBar");

const progressText =
    document.getElementById("progressText");

const questionCounter =
    document.getElementById("questionCounter");

const timerElement =
    document.getElementById("timer");

const technicalScore =
    document.getElementById("technicalScore");

const communicationScore =
    document.getElementById("communicationScore");

const confidenceScore =
    document.getElementById("confidenceScore");

const overallScore =
    document.getElementById("overallScore");

const liveScore =
    document.getElementById("liveScore");

// ======================================================
// GLOBAL STATE
// ======================================================

let elapsedSeconds = 0;

let currentQuestion = 1;

const TOTAL_QUESTIONS = 10;

let interviewCompleted = false;

// ======================================================
// TIMER
// ======================================================

function startTimer() {

    setInterval(() => {

        if (interviewCompleted)
            return;

        elapsedSeconds++;

        const minutes =
            String(
                Math.floor(elapsedSeconds / 60)
            ).padStart(2, "0");

        const seconds =
            String(
                elapsedSeconds % 60
            ).padStart(2, "0");

        timerElement.textContent =
            `${minutes}:${seconds}`;

    }, 1000);

}

// ======================================================
// UI HELPERS
// ======================================================

function showThinking(message = "Gemini is thinking...") {

    thinkingCard.classList.remove("hidden");

    aiStatus.textContent = message;

    submitButton.disabled = true;

    submitButton.classList.add(
        "opacity-50",
        "cursor-not-allowed"
    );

}

function hideThinking() {

    thinkingCard.classList.add("hidden");

    submitButton.disabled = false;

    submitButton.classList.remove(
        "opacity-50",
        "cursor-not-allowed"
    );

}

function showError(message) {

    hideThinking();

    alert(message);

}

function clearAnswerBox() {

    answerBox.value = "";

}

function disableControls() {

    submitButton.disabled = true;

    answerBox.disabled = true;

}

function enableControls() {

    submitButton.disabled = false;

    answerBox.disabled = false;

}

// ======================================================
// API
// ======================================================

async function submitCurrentAnswer() {

    const answer =
        answerBox.value.trim();

    if (answer.length === 0) {

        alert(
            "Please enter your answer first."
        );

        return;

    }

    showThinking(
        "Evaluating your answer..."
    );

    try {

        const response =
            await fetch(
                "/submit-answer",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body: JSON.stringify({

                        interview_id:
                            interviewId,

                        answer:
                            answer

                    })

                }
            );

        const data =
            await response.json();

        if (!response.ok) {

            throw new Error(
                data.error ||
                "Server Error"
            );

        }

        hideThinking();

        if (data.completed) {

            interviewCompleted = true;

            window.location.href =
                data.redirect;

            return;

        }

        updateInterviewUI(data);

        clearAnswerBox();

    }

    catch (error) {

        console.error(error);

        showError(
            error.message
        );

    }

}
// ======================================================
// UI UPDATE
// ======================================================

function updateInterviewUI(data) {

    currentQuestion =
        data.question_number;

    // -----------------------------
    // Question
    // -----------------------------

    questionElement.textContent =
        data.question;

    // -----------------------------
    // Progress
    // -----------------------------

    questionCounter.textContent =
        `Question ${currentQuestion}`;

    const percentage =
        (currentQuestion / TOTAL_QUESTIONS) * 100;

    progressBar.style.width =
        `${percentage}%`;

    progressText.textContent =
        `${currentQuestion} of ${TOTAL_QUESTIONS} questions completed`;

    // -----------------------------
    // Feedback
    // -----------------------------

    if (data.feedback) {

        feedbackCard.textContent =
            data.feedback;

    }

    // -----------------------------
    // Scores
    // -----------------------------

    if (data.technical_score !== undefined) {

        technicalScore.textContent =
            data.technical_score;

    }

    if (data.communication_score !== undefined) {

        communicationScore.textContent =
            data.communication_score;

    }

    if (data.confidence_score !== undefined) {

        confidenceScore.textContent =
            data.confidence_score;

    }

    if (data.overall_score !== undefined) {

        overallScore.textContent =
            data.overall_score;

        liveScore.textContent =
            data.overall_score;
    }

    // -----------------------------
    // Scroll to question
    // -----------------------------

    questionElement.scrollIntoView({

        behavior: "smooth",

        block: "center"

    });

}

// ======================================================
// EVENT LISTENERS
// ======================================================

submitButton.addEventListener(

    "click",

    submitCurrentAnswer

);

clearButton.addEventListener(

    "click",

    clearAnswerBox

);

answerBox.addEventListener(

    "keydown",

    function (event) {

        if (

            event.ctrlKey &&

            event.key === "Enter"

        ) {

            submitCurrentAnswer();

        }

    }

);

// ======================================================
// FINISH INTERVIEW
// ======================================================

finishButton.addEventListener(

    "click",

    function () {

        const confirmFinish =
            confirm(
                "Are you sure you want to finish the interview?"
            );

        if (!confirmFinish)
            return;

        interviewCompleted = true;

        disableControls();

        window.location.href =
            `/report/${interviewId}`;

    }

);

// ======================================================
// PAGE INITIALIZATION
// ======================================================

document.addEventListener(

    "DOMContentLoaded",

    function () {

        startTimer();

        progressBar.style.width =
            `${(currentQuestion / TOTAL_QUESTIONS) * 100}%`;

        feedbackCard.textContent =
            "Answer the current question to receive AI feedback.";

        console.log(

            "Interview Session Started",

            interviewId

        );

    }

);