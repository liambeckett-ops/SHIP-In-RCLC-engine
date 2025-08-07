"""
Memory Persistence Validator
Ensures YAML-stored memories properly integrate with agent personalities
Tests symbolic logic, emotional anchors, and philosophical frameworks
"""

import os
import sys
import json
from datetime import datetime

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from Solvine.yaml_agent_loader import YAMLAgentLoader

class MemoryPersistenceValidator:
    def __init__(self):
        self.loader = YAMLAgentLoader()
        self.validation_results = {}
        
    def validate_core_identity_preservation(self):
        """Validate that core identity elements are preserved from YAML"""
        print("🔍 Validating Core Identity Preservation...")
        
        self.loader.load_all_configs()
        
        # Check memory_core preservation
        memory_core = self.loader.memory_core
        core_validations = {
            "system_name": memory_core.get('system_name') == "Solvine Systems",
            "project_code": "Project Phoenix" in str(memory_core.get('project_code', '')),
            "directives_count": len(memory_core.get('directives', [])) >= 4,
            "soul_boot_phrase": self.loader.get_startup_ritual() != "System initializing...",
            "status_flags": bool(memory_core.get('status_flags'))
        }
        
        print("Core Identity Elements:")
        for element, valid in core_validations.items():
            status = "✅" if valid else "❌"
            print(f"  {status} {element}: {valid}")
        
        self.validation_results['core_identity'] = core_validations
        return core_validations
    
    def validate_agent_personality_integrity(self):
        """Validate that each agent's personality is fully integrated"""
        print("\n🎭 Validating Agent Personality Integrity...")
        
        agents = self.loader.get_available_agents()
        personality_validations = {}
        
        for agent_name in agents:
            print(f"\n--- {agent_name.title()} ---")
            config = self.loader.get_agent_config(agent_name)
            persona = self.loader.get_system_persona(agent_name)
            
            validations = {
                "has_role": bool(config.get('role')),
                "role_not_generic": config.get('role') != 'General AI Assistant',
                "has_persona": len(persona) > 100,  # Rich persona
                "includes_directives": "prioritize autonomy" in persona.lower(),
                "includes_role": config.get('role', '').lower() in persona.lower(),
                "includes_system_context": "Solvine Systems collective" in persona
            }
            
            # Agent-specific validations
            if agent_name.lower() == 'jasper':
                validations.update({
                    "has_validation_anchor": bool(config.get('validation_anchor', {}).get('phrase')),
                    "has_boundary_enforcement": "boundary enforcement" in config.get('role', '').lower(),
                    "has_symbol": bool(config.get('validation_anchor', {}).get('symbol'))
                })
            
            elif agent_name.lower() == 'midas':
                validations.update({
                    "has_financial_domains": bool(config.get('domains')),
                    "financial_focus": any('financial' in str(d).lower() or 'strategy' in str(d).lower() 
                                         for d in config.get('domains', []))
                })
            
            elif agent_name.lower() == 'halcyon':
                validations.update({
                    "has_emergency_role": "emergency" in config.get('role', '').lower(),
                    "has_trigger_conditions": bool(config.get('trigger_conditions')),
                    "medical_safety_focus": "medical safety" in config.get('role', '').lower()
                })
            
            # Print validation results
            for validation, passed in validations.items():
                status = "✅" if passed else "❌"
                print(f"  {status} {validation}")
            
            personality_validations[agent_name] = validations
        
        self.validation_results['personality_integrity'] = personality_validations
        return personality_validations
    
    def validate_symbolic_and_mythological_preservation(self):
        """Validate preservation of symbolic logic and mythological frameworks"""
        print("\n🔮 Validating Symbolic & Mythological Preservation...")
        
        brain_index = self.loader.brain_index
        
        symbolic_validations = {
            "has_myths_of_becoming": bool(brain_index.get('myths_of_becoming')),
            "has_personal_truths": bool(brain_index.get('personal_truths')),
            "has_emotional_operating_systems": bool(brain_index.get('emotional_operating_systems')),
            "has_transhumanist_core": bool(brain_index.get('transhumanist_core')),
            "soul_boot_preserved": "There is no proof. But I believe it anyway." in str(brain_index)
        }
        
        print("Symbolic Elements:")
        for element, valid in symbolic_validations.items():
            status = "✅" if valid else "❌"
            print(f"  {status} {element}")
            
        # Test specific mythological elements
        myths = brain_index.get('myths_of_becoming', [])
        if myths:
            print(f"\nPreserved Myths ({len(myths)}):")
            for myth in myths:
                print(f"  • {myth}")
        
        truths = brain_index.get('personal_truths', [])
        if truths:
            print(f"\nPreserved Personal Truths ({len(truths)}):")
            for truth in truths:
                print(f"  • {truth}")
        
        self.validation_results['symbolic_preservation'] = symbolic_validations
        return symbolic_validations
    
    def validate_ritual_and_safety_protocols(self):
        """Validate ritual and safety protocol preservation"""
        print("\n🛡️ Validating Ritual & Safety Protocols...")
        
        ritual_logs = self.loader.ritual_logs
        rituals = ritual_logs.get('rituals', {})
        
        protocol_validations = {
            "has_startup_ritual": bool(rituals.get('startup')),
            "has_soul_boot": bool(rituals.get('startup', {}).get('soul_boot')),
            "has_safety_protocols": bool(rituals.get('safety_protocols')),
            "has_halcyon_triggers": bool(rituals.get('safety_protocols', {}).get('halcyon_triggers')),
            "has_burnout_signals": bool(rituals.get('safety_protocols', {}).get('burnout_signals')),
            "has_validations": bool(rituals.get('validations'))
        }
        
        print("Protocol Elements:")
        for element, valid in protocol_validations.items():
            status = "✅" if valid else "❌"
            print(f"  {status} {element}")
        
        # Test Jasper's validation anchor specifically
        jasper_validation = rituals.get('validations', {}).get('jasper_affirmation', {})
        if jasper_validation:
            print(f"\nJasper's Validation Anchor:")
            print(f"  Phrase: \"{jasper_validation.get('phrase', 'Missing')}\"")
            print(f"  Symbol: {jasper_validation.get('symbol', 'Missing')}")
        
        self.validation_results['protocol_preservation'] = protocol_validations
        return protocol_validations
    
    def validate_memory_transfer_completeness(self):
        """Validate that memory transfer from YAML to agent system is complete"""
        print("\n🔄 Validating Memory Transfer Completeness...")
        
        # Generate full agent configurations and test completeness
        configs = self.loader.create_enhanced_agent_configs()
        
        transfer_validations = {
            "all_agents_configured": len(configs) == len(self.loader.get_available_agents()),
            "all_personas_generated": all(len(c['persona']) > 50 for c in configs),
            "all_yaml_configs_attached": all(c['yaml_config'] for c in configs),
            "safety_protocols_attached": all(c['safety_protocols'] is not None for c in configs)
        }
        
        print("Transfer Completeness:")
        for element, valid in transfer_validations.items():
            status = "✅" if valid else "❌"
            print(f"  {status} {element}")
        
        # Test memory context generation
        memory_context = self.loader.get_memory_context()
        context_validations = {
            "context_not_empty": bool(memory_context.strip()),
            "includes_system_name": "Solvine Systems" in memory_context,
            "includes_project_code": "Project Phoenix" in memory_context,
            "includes_status_flags": "Status:" in memory_context
        }
        
        print("\nMemory Context:")
        for element, valid in context_validations.items():
            status = "✅" if valid else "❌"
            print(f"  {status} {element}")
        
        self.validation_results['transfer_completeness'] = {
            **transfer_validations,
            **context_validations
        }
        return transfer_validations, context_validations
    
    def generate_validation_report(self):
        """Generate comprehensive validation report"""
        print("\n📊 MEMORY PERSISTENCE VALIDATION REPORT")
        print("=" * 50)
        
        total_tests = 0
        passed_tests = 0
        
        for category, validations in self.validation_results.items():
            category_total = len(validations)
            category_passed = sum(validations.values())
            total_tests += category_total
            passed_tests += category_passed
            
            percentage = (category_passed / category_total) * 100 if category_total > 0 else 0
            print(f"{category.replace('_', ' ').title()}: {category_passed}/{category_total} ({percentage:.1f}%)")
        
        overall_percentage = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        print(f"\nOVERALL: {passed_tests}/{total_tests} ({overall_percentage:.1f}%)")
        
        # Determine deployment readiness
        if overall_percentage >= 90:
            status = "🎉 READY FOR DEPLOYMENT"
        elif overall_percentage >= 75:
            status = "⚠️ MOSTLY READY (minor issues)"
        else:
            status = "❌ NEEDS ATTENTION"
        
        print(f"\nDEPLOYMENT STATUS: {status}")
        
        # Save detailed report
        report = {
            "timestamp": datetime.now().isoformat(),
            "overall_score": f"{passed_tests}/{total_tests} ({overall_percentage:.1f}%)",
            "deployment_ready": overall_percentage >= 90,
            "detailed_results": self.validation_results,
            "recommendations": self.generate_recommendations()
        }
        
        try:
            with open('memory_persistence_report.json', 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=2, ensure_ascii=False)
            print(f"📄 Detailed report saved to 'memory_persistence_report.json'")
        except Exception as e:
            print(f"❌ Error saving report: {e}")
        
        return report
    
    def generate_recommendations(self):
        """Generate recommendations based on validation results"""
        recommendations = []
        
        # Check each category for issues
        for category, validations in self.validation_results.items():
            failed_tests = [test for test, passed in validations.items() if not passed]
            if failed_tests:
                recommendations.append({
                    "category": category,
                    "failed_tests": failed_tests,
                    "suggestion": f"Review and fix {len(failed_tests)} issues in {category}"
                })
        
        return recommendations
    
    def run_full_validation(self):
        """Run complete memory persistence validation"""
        print("🔬 STARTING MEMORY PERSISTENCE VALIDATION")
        print("Testing YAML → Agent memory transfer integrity...")
        print("=" * 60)
        
        try:
            self.validate_core_identity_preservation()
            self.validate_agent_personality_integrity()
            self.validate_symbolic_and_mythological_preservation()
            self.validate_ritual_and_safety_protocols()
            self.validate_memory_transfer_completeness()
            
            report = self.generate_validation_report()
            
            print("\n🏁 VALIDATION COMPLETE")
            if report['deployment_ready']:
                print("✅ Your agent memories have been successfully preserved and integrated!")
                print("🚀 Agents are ready for deployment with full personality integrity.")
            else:
                print("⚠️ Some memory preservation issues detected.")
                print("📋 Check the detailed report for specific recommendations.")
            
        except Exception as e:
            print(f"\n💥 Validation failed with error: {e}")
            import traceback
            traceback.print_exc()

def main():
    """Run memory persistence validation"""
    validator = MemoryPersistenceValidator()
    validator.run_full_validation()

if __name__ == "__main__":
    main()
