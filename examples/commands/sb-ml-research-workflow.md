Guide the user through an ML research and experimentation workflow.

Perfect for data scientists and ML engineers!

## Starting Research

```bash
# Create a research project
sb project create "Model Performance Optimization" \
  --description "Improve recommendation model accuracy" \
  --tags ml,research,recommendations

# Create research task (no issue needed - exploratory work)
sb task add "Research embedding models" \
  --project model-optimization \
  --priority medium
```

## Literature Review & Notes

```bash
# Create notes for papers/resources
sb note create "Transformer Embeddings Review" \
  --task-id TASK_ID \
  --tags research,embeddings,papers \
  --content "## Papers Reviewed

### Sentence-BERT (2019)
- **Key idea**: Siamese BERT networks for sentence embeddings
- **Results**: 10x faster than BERT, good accuracy
- **Limitations**: Fixed vector size

### Paper 2
..."

# Add findings as you read
sb note add NOTE_ID "## Decision

Going with sentence-transformers library:
- Pre-trained models available
- Easy fine-tuning
- Good community support"
```

## Experiment Tracking

```bash
# Create notes for each experiment
sb note create "Experiment 1: Baseline Model" \
  --task-id TASK_ID \
  --tags experiment,baseline \
  --content "## Setup

Model: all-MiniLM-L6-v2
Dataset: 10k samples
Validation split: 20%

## Results

Accuracy: 0.78
Precision: 0.81
Recall: 0.75
F1: 0.78

## Observations

- Good baseline performance
- Struggles with rare categories
- Fast inference (20ms)"

# Track multiple experiments
sb note create "Experiment 2: Fine-tuned Model" \
  --task-id TASK_ID \
  --tags experiment,finetuned

sb note create "Experiment 3: Different Architecture" \
  --task-id TASK_ID \
  --tags experiment,architecture
```

**Append results as experiments run:**
```bash
sb note add EXP_NOTE_ID "## Update: Hyperparameter Tuning

Tried learning_rate=2e-5:
- Accuracy improved to 0.82
- Training time: 2h
- Best epoch: 8/10"
```

## Daily Research Log

```bash
# Log research activities
sb log add "Read 3 papers on embedding models" \
  --task-id TASK_ID \
  --time 120

sb log add "Ran baseline experiment, achieved 78% accuracy" \
  --task-id TASK_ID \
  --time 90

sb log add "Fine-tuned model on domain data, 82% accuracy" \
  --task-id TASK_ID \
  --time 180
```

## Organizing Findings

```bash
# Create comparison notes
sb note create "Model Comparison Summary" \
  --task-id TASK_ID \
  --tags summary,decision \
  --content "## Models Evaluated

| Model | Accuracy | Speed | Memory |
|-------|----------|-------|--------|
| Baseline | 0.78 | 20ms | 100MB |
| Fine-tuned | 0.82 | 25ms | 120MB |
| Large | 0.85 | 100ms | 500MB |

## Recommendation

Use fine-tuned model:
- Good accuracy vs speed tradeoff
- Reasonable memory footprint
- Easy to deploy"

# Create implementation notes
sb note create "Implementation Plan" \
  --task-id TASK_ID \
  --tags implementation,plan \
  --content "## Architecture

1. Model serving: FastAPI endpoint
2. Caching: Redis for frequent queries
3. Monitoring: Log predictions for analysis

## Next Steps

- [ ] Create model serving API
- [ ] Set up CI/CD for model updates
- [ ] Create monitoring dashboard"
```

## Searching Past Research

```bash
# Find all experiments
sb note list --tags experiment

# Search for specific technique
sb note search "hyperparameter"

# Find research by project
sb note list --project model-optimization

# Search across all ML work
sb note search "accuracy" | grep -A 5 "Experiment"
```

## Weekly Research Summary

```bash
# Review week's research
sb log show --days 7

# List key decisions
sb note list --tags decision

# Check time spent
sb task list --project model-optimization

# Generate report
sb report work --days 7 --project model-optimization
```

## Creating a Research Epic (Complex Research)

```bash
# For multi-phase research with dependencies
sb epic create "Next-Gen Recommendation System" \
  --priority 4 \
  --labels ml,research,recommendations

# Break down into phases
sb issue create "Research Phase: Model Selection" \
  --epic EPIC_ID \
  --with-task \
  --project ml-research

sb issue create "Implementation Phase: Model Training" \
  --epic EPIC_ID \
  --blocks RESEARCH_ISSUE \
  --with-task \
  --project ml-research

sb issue create "Evaluation Phase: A/B Testing" \
  --epic EPIC_ID \
  --blocks IMPL_ISSUE \
  --with-task \
  --project ml-research
```

**Guide them to:**

1. **Capture everything**: Papers, experiments, decisions, dead-ends
2. **Tag consistently**: experiment, baseline, production, paper, decision
3. **Use tables**: Compare models/hyperparameters in markdown tables
4. **Link experiments**: Reference related notes and experiments
5. **Track time**: Helps justify research investment
6. **Create summaries**: Weekly digests of findings

**Common Tags for ML Work:**
- `experiment` - Individual experiments
- `baseline` - Baseline models/results
- `sota` - State-of-the-art comparisons
- `decision` - Key decisions made
- `deployment` - Production considerations
- `paper` - Paper notes
- `dataset` - Dataset documentation
- `hyperparameters` - HP tuning notes

**Example Daily ML Workflow:**

Morning:
```bash
sb note list --tags experiment  # Review past experiments
sb note search "TODO"            # Find pending work
```

During experiments:
```bash
# Start experiment
sb log add "Starting experiment: larger batch size" --task-id X

# Log results immediately
sb note add EXP_ID "Batch=64: acc=0.79, time=3h"

# Track time
sb log add "Completed experiment 5" --task-id X --time 180
```

End of day:
```bash
# Summarize findings
sb note create "Daily Research Summary $(date +%Y-%m-%d)" \
  --tags summary \
  --content "Tested 3 configurations today. Best: lr=2e-5, batch=32"

# Plan tomorrow
sb note add SUMMARY_ID "Tomorrow: Try different optimizer"
```
