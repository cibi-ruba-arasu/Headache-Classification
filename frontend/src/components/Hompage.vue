<template>
  <div class="medical-wrapper">
    <div class="container">
      <header class="header">
        <h1 class="clinical-title">Headache Symptom Assessment</h1>
        <p class="subtitle">Please indicate your current symptoms below to receive a preliminary clinical classification.</p>
      </header>

      <form @submit.prevent="submitSymptoms" class="symptom-form">
        <!-- Dynamic Form Generation -->
        <div 
          v-for="(field, index) in symptomConfig" 
          :key="field.key" 
          class="question-card"
        >
          <h3 class="question-title">{{ formatLabel(field.key) }}</h3>
          <p class="question-desc">{{ field.description }}</p>
          
          <div class="options-grid" :class="{ 'yes-no-grid': field.options.length === 2 }">
            <label 
              v-for="option in field.options" 
              :key="option" 
              class="option-label"
              :class="{ 'selected': formData[field.key] === option }"
            >
              <input 
                type="radio" 
                :name="field.key" 
                :value="option" 
                v-model="formData[field.key]" 
                required
              />
              <span class="option-text">{{ option }}</span>
            </label>
          </div>
        </div>

        <button type="submit" class="submit-btn" :disabled="isLoading">
          <span v-if="!isLoading">Analyze Symptoms</span>
          <span v-else class="pulsing">Processing data...</span>
        </button>
      </form>

      <!-- Results Panel -->
      <div v-if="predictionResult" class="result-panel">
        <div class="result-header">
          <svg class="success-icon" viewBox="0 0 24 24" width="28" height="28">
            <path fill="currentColor" d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
          </svg>
          <h2>Evaluation Complete</h2>
        </div>
        <div class="result-content">
          <p class="result-text">Preliminary Classification: <span class="highlight">{{ predictionResult }}</span></p>
        </div>
        <div class="disclaimer">
          <strong>Medical Disclaimer:</strong> This is an AI-generated assessment tool and does not constitute professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
        </div>
        <button @click="resetForm" class="reset-btn">Start New Assessment</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue';

const isLoading = ref(false);
const predictionResult = ref(null);

const formData = reactive({
  Pain_Type: '',
  Pain_Location: '',
  Pain_Duration: '',
  Onset_Speed: '',
  Nausea_Vomiting: '',
  Light_Sound_Sensitivity: '',
  Visual_Aura_or_Changes: '',
  Nasal_Congestion_Tearing: '',
  Recent_Head_Injury: '',
  Recent_Physical_Exertion: '',
  Medication_Overuse: '',
  Caffeine_Withdrawal: '',
  Menstruation_or_Hormones: '',
  High_Blood_Pressure: '',
  Recent_Lumbar_Puncture: '',
  Worsens_Upright: ''
});

// Dictionary dictating the form rendering, now with helper descriptions
const symptomConfig = [
  { 
    key: 'Pain_Type', 
    options: ['Dull/Aching', 'Burning/Piercing', 'Throbbing/Pulsing', 'Stabbing', 'Severe'],
    description: 'Select the word that best describes the primary sensation of your pain.'
  },
  { 
    key: 'Pain_Location', 
    options: ['All over', 'Back of head/Neck', 'Both sides', 'Around one eye', 'One side', 'Moves around', 'Sinus/Front'],
    description: 'Indicate where the pain is primarily focused on your head or face.'
  },
  { 
    key: 'Pain_Duration', 
    options: ['Minutes to Hours', '4 to 72 hours', 'Continuous (>3 months)', 'Seconds'],
    description: 'Estimate how long a typical headache episode lasts without medication.'
  },
  { 
    key: 'Onset_Speed', 
    options: ['Gradual', 'Rapid (Under 1 min)'],
    description: 'Describe how quickly the headache reaches its maximum intensity.'
  },
  { 
    key: 'Nausea_Vomiting', 
    options: ['No', 'Yes'],
    description: 'Do you experience stomach discomfort or vomiting during the headache?'
  },
  { 
    key: 'Light_Sound_Sensitivity', 
    options: ['No', 'Yes'],
    description: 'Does exposure to normal light or sound make your headache significantly worse?'
  },
  { 
    key: 'Visual_Aura_or_Changes', 
    options: ['No', 'Yes'],
    description: 'Have you noticed flashing lights, blind spots, or other visual disturbances before or during the headache?'
  },
  { 
    key: 'Nasal_Congestion_Tearing', 
    options: ['No', 'Yes'],
    description: 'Do you experience a runny nose, stuffiness, or watery eyes, particularly on the same side as the headache?'
  },
  { 
    key: 'Recent_Head_Injury', 
    options: ['No', 'Yes'],
    description: 'Did this headache pattern begin following a recent physical impact or trauma to the head?'
  },
  { 
    key: 'Recent_Physical_Exertion', 
    options: ['No', 'Yes'],
    description: 'Did the headache start during or immediately after intense physical activity, such as exercising, lifting, or intercourse?'
  },
  { 
    key: 'Medication_Overuse', 
    options: ['No', 'Yes'],
    description: 'Do you take over-the-counter pain relievers for headaches more than 15 days a month?'
  },
  { 
    key: 'Caffeine_Withdrawal', 
    options: ['No', 'Yes'],
    description: 'Did the headache start after missing or significantly reducing your usual caffeine intake (e.g., coffee, tea, energy drinks)?'
  },
  { 
    key: 'Menstruation_or_Hormones', 
    options: ['No', 'Yes'],
    description: 'Does the headache regularly occur close to or during your menstrual cycle, or align with hormonal fluctuations?'
  },
  { 
    key: 'High_Blood_Pressure', 
    options: ['No', 'Yes'],
    description: 'Do you have diagnosed severe high blood pressure, or did a recent reading show dangerously high levels (e.g., greater than 180/120)?'
  },
  { 
    key: 'Recent_Lumbar_Puncture', 
    options: ['No', 'Yes'],
    description: 'Have you recently had a spinal tap (lumbar puncture), epidural injection, or spinal anesthesia?'
  },
  { 
    key: 'Worsens_Upright', 
    options: ['No', 'Yes'],
    description: 'Does the pain get significantly worse when you stand or sit up, and notably improve when you lie completely flat?'
  }
];

const formatLabel = (key) => {
  return key.replace(/_/g, ' ') + '?';
};

const submitSymptoms = async () => {
  isLoading.value = true;
  predictionResult.value = null;

  try {
    const formattedPayload = {};
    for (const [key, value] of Object.entries(formData)) {
      formattedPayload[key] = [value];
    }

    const response = await fetch('http://localhost:5000/api/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formattedPayload)
    });

    if (!response.ok) throw new Error('Failed to reach the backend');
    
    const data = await response.json();
    predictionResult.value = data.prediction; 

  } catch (error) {
    console.error("Error during prediction fetch:", error);
    predictionResult.value = "A network error occurred. Please verify your connection and try again.";
  } finally {
    isLoading.value = false;
  }
};

const resetForm = () => {
  predictionResult.value = null;
  Object.keys(formData).forEach(key => formData[key] = '');
  window.scrollTo({ top: 0, behavior: 'smooth' });
};
</script>

<style scoped>
/* Base Clinical Theme */
.medical-wrapper {
  min-height: 100vh;
  background-color: #f4f7f9;
  color: #333333;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  padding: 40px 20px;
  line-height: 1.6;
}

.container {
  max-width: 800px;
  margin: 0 auto;
}

/* Header Styling */
.header {
  text-align: center;
  margin-bottom: 40px;
}

.clinical-title {
  color: #004085;
  font-size: 2.2rem;
  font-weight: 600;
  margin-bottom: 10px;
}

.subtitle {
  color: #6c757d;
  font-size: 1.1rem;
}

/* Question Cards */
.question-card {
  background: #ffffff;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.question-title {
  color: #212529;
  margin-top: 0;
  margin-bottom: 6px; /* Reduced to make room for description */
  font-size: 1.1rem;
  font-weight: 600;
  text-transform: capitalize;
}

.question-desc {
  color: #6c757d;
  font-size: 0.95rem;
  margin-top: 0;
  margin-bottom: 18px;
  line-height: 1.4;
}

/* Selection Grid */
.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
}

.yes-no-grid {
  grid-template-columns: repeat(2, 1fr);
}

.option-label {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  border: 1px solid #ced4da;
  border-radius: 6px;
  padding: 12px;
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  text-align: center;
  font-weight: 500;
  color: #495057;
}

.option-label input[type="radio"] {
  display: none;
}

.option-label:hover {
  background: #e2e6ea;
}

.option-label.selected {
  background: #e6f2ff;
  border-color: #007bff;
  color: #0056b3;
  box-shadow: 0 0 0 1px #007bff;
}

/* Submit Button */
.submit-btn {
  width: 100%;
  padding: 16px;
  font-size: 1.1rem;
  font-weight: 600;
  background: #007bff;
  color: #ffffff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 10px;
  transition: background-color 0.2s ease;
  box-shadow: 0 4px 6px rgba(0, 123, 255, 0.2);
}

.submit-btn:hover:not(:disabled) {
  background: #0056b3;
}

.submit-btn:disabled {
  background: #6c757d;
  cursor: not-allowed;
  box-shadow: none;
}

/* Results Panel */
.result-panel {
  margin-top: 40px;
  padding: 32px;
  background: #ffffff;
  border-left: 5px solid #28a745;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.result-header {
  display: flex;
  align-items: center;
  color: #28a745;
  margin-bottom: 20px;
}

.result-header h2 {
  margin: 0 0 0 10px;
  font-size: 1.5rem;
}

.result-content {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 6px;
  border: 1px solid #e9ecef;
  margin-bottom: 24px;
}

.result-text {
  font-size: 1.2rem;
  margin: 0;
  color: #333333;
}

.highlight {
  color: #004085;
  font-weight: 700;
  font-size: 1.4rem;
  display: block;
  margin-top: 8px;
}

.disclaimer {
  font-size: 0.9rem;
  color: #6c757d;
  background: #fff3cd;
  border: 1px solid #ffeeba;
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 24px;
}

.reset-btn {
  background: transparent;
  color: #007bff;
  border: 1px solid #007bff;
  padding: 12px 24px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
}

.reset-btn:hover {
  background: #007bff;
  color: #ffffff;
}

.pulsing {
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}
</style>