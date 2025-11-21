#!/usr/bin/env python3
"""
Train WalterSignal Design Crew for Website Deployment
Loads training cases and trains the 4-agent design crew
"""

import yaml
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from crews.waltersignal_design.waltersignal_design_crew import create_waltersignal_design_crew

def load_training_data():
    """Load training cases from YAML"""
    training_file = Path(__file__).parent / "waltersignal_design_deployment_training.yaml"

    with open(training_file, 'r') as f:
        data = yaml.safe_load(f)

    return data

def train_crew_with_case(case):
    """Train crew with a single training case"""
    print(f"\n{'='*80}")
    print(f"🎓 Training Case: {case['task_id']}")
    print(f"Agent: {case['agent']}")
    print('='*80)
    print(f"\n📝 Task: {case['task_description'][:200]}...")

    # Create crew for this task
    crew = create_waltersignal_design_crew(
        task_description=case['task_description'],
        expected_output=case['expected_output'],
        agent_id=case['agent'],
        use_manager=False  # Sequential mode for training
    )

    # Execute the task
    print(f"\n🚀 Executing training task...")
    result = crew.kickoff()

    # Compare result with expected outcome
    print(f"\n✅ Training Complete")
    print(f"\nExpected Outcome:")
    print(case['learned_outcome'][:300] + "...")

    print(f"\nActual Result:")
    print(str(result)[:300] + "...")

    # Extract quality metrics
    print(f"\n📊 Quality Metrics:")
    for metric, target in case['quality_metrics'].items():
        print(f"  - {metric}: {target}")

    return result

def main():
    """Main training function"""
    print("\n" + "="*80)
    print("🎨 WALTERSIGNAL DESIGN CREW TRAINING")
    print("="*80)
    print("\nTraining the 4-agent design crew for website deployment...")

    # Load training data
    print("\n📚 Loading training data...")
    training_data = load_training_data()

    cases = training_data['training_cases']
    print(f"✅ Loaded {len(cases)} training cases")

    # Display training overview
    print(f"\n📋 Training Cases:")
    for i, case in enumerate(cases, 1):
        print(f"  {i}. {case['task_id']}: {case['agent']}")

    # Ask user which case to train
    print(f"\nOptions:")
    print(f"  1-{len(cases)}: Train specific case")
    print(f"  all: Train all cases sequentially")
    print(f"  q: Quit")

    choice = input(f"\nSelect option: ").strip().lower()

    if choice == 'q':
        print("👋 Training cancelled")
        return

    elif choice == 'all':
        print(f"\n🚀 Training all {len(cases)} cases...")

        for i, case in enumerate(cases, 1):
            print(f"\n\n{'#'*80}")
            print(f"# CASE {i}/{len(cases)}")
            print('#'*80)

            try:
                result = train_crew_with_case(case)

                # Save training result
                output_dir = Path(__file__).parent.parent / "outputs" / "training"
                output_dir.mkdir(parents=True, exist_ok=True)

                output_file = output_dir / f"{case['task_id']}_training_result.txt"
                with open(output_file, 'w') as f:
                    f.write(f"Training Case: {case['task_id']}\n")
                    f.write(f"Agent: {case['agent']}\n")
                    f.write(f"\nTask Description:\n{case['task_description']}\n")
                    f.write(f"\nExpected Output:\n{case['expected_output']}\n")
                    f.write(f"\nActual Result:\n{str(result)}\n")
                    f.write(f"\nLearned Outcome:\n{case['learned_outcome']}\n")

                print(f"\n✅ Result saved to: {output_file}")

            except Exception as e:
                print(f"\n❌ Training failed for {case['task_id']}: {e}")
                continue

        print(f"\n\n{'='*80}")
        print(f"✅ TRAINING COMPLETE - All {len(cases)} cases executed")
        print('='*80)

    else:
        try:
            case_num = int(choice) - 1
            if 0 <= case_num < len(cases):
                case = cases[case_num]
                result = train_crew_with_case(case)

                # Save result
                output_dir = Path(__file__).parent.parent / "outputs" / "training"
                output_dir.mkdir(parents=True, exist_ok=True)

                output_file = output_dir / f"{case['task_id']}_training_result.txt"
                with open(output_file, 'w') as f:
                    f.write(str(result))

                print(f"\n✅ Result saved to: {output_file}")
            else:
                print(f"❌ Invalid case number")
        except ValueError:
            print(f"❌ Invalid input")

if __name__ == "__main__":
    main()
