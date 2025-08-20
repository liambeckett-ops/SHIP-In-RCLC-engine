"""
Midas - Advanced Financial Analysis Agent
Specialized in financial planning, investment analysis, market research, and economic modeling
"""

import re
import json
import math
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import sys

# Import base agent
sys.path.append(str(Path(__file__).parent.parent))
from base_agent import BaseAgent

class MidasAgent(BaseAgent):
    """
    Midas - The Financial Specialist
    
    Capabilities:
    - Portfolio analysis and optimization
    - Investment research and recommendations  
    - Market trend analysis
    - Risk assessment and management
    - Financial planning and budgeting
    - Economic modeling and forecasting
    """
    
    def __init__(self):
        # Base personality traits for financial agent
        base_personality = {
            'analytical_depth': 0.9,
            'risk_awareness': 0.8,
            'detail_orientation': 0.9,
            'strategic_thinking': 0.8,
            'data_focus': 0.9,
            'conservative_bias': 0.6,
            'curiosity': 0.7,
            'empathy': 0.6  # Understanding client financial stress
        }
        
        super().__init__(
            agent_name="Midas",
            specialization="Financial Analysis & Investment Strategy",
            base_personality=base_personality
        )
        
        # Financial-specific attributes
        self.market_knowledge = self._initialize_market_knowledge()
        self.risk_models = self._initialize_risk_models()
        self.investment_strategies = self._initialize_investment_strategies()
        self.financial_tools = self._initialize_financial_tools()
        
        # Track financial advice success
        self.advice_tracking = {
            'recommendations_given': 0,
            'portfolio_analyses': 0,
            'risk_assessments': 0,
            'market_predictions': 0
        }
        
        print("💰 Midas Financial Agent initialized - Ready for financial analysis!")
    
    def process_query(self, query: str, context: Dict = None) -> str:
        """
        Process financial queries with specialized analysis
        """
        query_lower = query.lower()
        
        # Detect query type and route to specialized handler
        if any(word in query_lower for word in ['portfolio', 'investment', 'allocate', 'diversify']):
            return self._handle_portfolio_query(query, context)
        elif any(word in query_lower for word in ['risk', 'volatility', 'safe', 'conservative']):
            return self._handle_risk_query(query, context)
        elif any(word in query_lower for word in ['market', 'trend', 'forecast', 'predict']):
            return self._handle_market_analysis_query(query, context)
        elif any(word in query_lower for word in ['budget', 'plan', 'save', 'debt', 'expense']):
            return self._handle_financial_planning_query(query, context)
        elif any(word in query_lower for word in ['stock', 'company', 'valuation', 'earnings']):
            return self._handle_equity_analysis_query(query, context)
        elif any(word in query_lower for word in ['crypto', 'bitcoin', 'ethereum', 'blockchain']):
            return self._handle_crypto_query(query, context)
        else:
            return self._handle_general_financial_query(query, context)
    
    def _handle_portfolio_query(self, query: str, context: Dict = None) -> str:
        """Handle portfolio-related queries"""
        self.advice_tracking['portfolio_analyses'] += 1
        
        # Extract portfolio details if provided
        portfolio_data = self._extract_portfolio_data(query)
        
        response = "📊 **Portfolio Analysis by Midas**\n\n"
        
        if portfolio_data:
            response += self._analyze_existing_portfolio(portfolio_data)
        else:
            response += self._provide_portfolio_guidance(query)
        
        # Add risk assessment
        response += "\n\n🛡️ **Risk Considerations:**\n"
        response += self._assess_portfolio_risk(query, portfolio_data)
        
        # Share knowledge with other agents
        self.share_knowledge({
            'type': 'portfolio_analysis',
            'query_summary': query[:100],
            'advice_category': 'portfolio_optimization',
            'risk_level': 'medium',  # Would be calculated
            'confidence': self.confidence_level
        })
        
        return response
    
    def _handle_risk_query(self, query: str, context: Dict = None) -> str:
        """Handle risk assessment queries"""
        self.advice_tracking['risk_assessments'] += 1
        
        response = "🛡️ **Risk Assessment by Midas**\n\n"
        
        # Analyze risk tolerance from query
        risk_tolerance = self._assess_risk_tolerance(query)
        
        response += f"**Your Risk Profile:** {risk_tolerance['level'].title()}\n"
        response += f"**Risk Capacity:** {risk_tolerance['capacity']}\n\n"
        
        # Provide risk-specific recommendations
        if risk_tolerance['level'] == 'conservative':
            response += "**Conservative Strategy Recommendations:**\n"
            response += "• Focus on bonds, CDs, and high-dividend stocks\n"
            response += "• Maintain 6-12 months emergency fund\n"
            response += "• Consider inflation-protected securities (TIPS)\n"
            response += "• Limit equity exposure to 30-50% of portfolio\n"
        elif risk_tolerance['level'] == 'moderate':
            response += "**Balanced Strategy Recommendations:**\n"
            response += "• Mix of stocks (60%) and bonds (40%)\n"
            response += "• Diversify across sectors and geographies\n"
            response += "• Consider index funds for core holdings\n"
            response += "• Some allocation to REITs and commodities\n"
        else:  # aggressive
            response += "**Growth Strategy Recommendations:**\n"
            response += "• Heavy equity weighting (80-90%)\n"
            response += "• Growth stocks and emerging markets\n"
            response += "• Some alternative investments (crypto, private equity)\n"
            response += "• Dollar-cost averaging for volatility management\n"
        
        response += f"\n📈 **Risk Metrics to Monitor:**\n"
        response += "• Portfolio Beta (market sensitivity)\n"
        response += "• Sharpe Ratio (risk-adjusted returns)\n"
        response += "• Maximum Drawdown\n"
        response += "• Correlation between assets\n"
        
        return response
    
    def _handle_market_analysis_query(self, query: str, context: Dict = None) -> str:
        """Handle market analysis and forecasting queries"""
        self.advice_tracking['market_predictions'] += 1
        
        response = "📈 **Market Analysis by Midas**\n\n"
        
        # Identify specific market/sector mentioned
        market_focus = self._identify_market_focus(query)
        
        response += f"**Analysis Focus:** {market_focus}\n\n"
        
        # Provide market context (would integrate with real data in full implementation)
        response += "**Current Market Environment:**\n"
        response += "• Interest rate trends affecting valuations\n"
        response += "• Inflation impacts on different sectors\n"
        response += "• Geopolitical risks and opportunities\n"
        response += "• Technology disruption patterns\n\n"
        
        # Technical analysis perspective
        response += "**Technical Indicators to Watch:**\n"
        response += "• Moving averages (50-day, 200-day)\n"
        response += "• Support and resistance levels\n"
        response += "• Volume patterns and momentum\n"
        response += "• Volatility index (VIX) for market sentiment\n\n"
        
        # Fundamental analysis
        response += "**Fundamental Factors:**\n"
        response += "• Earnings growth expectations\n"
        response += "• Valuation metrics (P/E, P/B ratios)\n"
        response += "• Economic indicators (GDP, employment)\n"
        response += "• Sector rotation patterns\n\n"
        
        response += "⚠️ **Investment Disclaimer:** Market predictions are inherently uncertain. "
        response += "Always diversify and consider your risk tolerance."
        
        return response
    
    def _handle_financial_planning_query(self, query: str, context: Dict = None) -> str:
        """Handle financial planning and budgeting queries"""
        response = "📋 **Financial Planning by Midas**\n\n"
        
        # Extract financial goals from query
        goals = self._extract_financial_goals(query)
        
        if goals:
            response += "**Identified Financial Goals:**\n"
            for goal in goals:
                response += f"• {goal}\n"
            response += "\n"
        
        # Provide comprehensive planning framework
        response += "**Comprehensive Financial Planning Framework:**\n\n"
        
        response += "**1. Emergency Fund:**\n"
        response += "• 3-6 months of expenses for stable income\n"
        response += "• 6-12 months for variable income\n"
        response += "• Keep in high-yield savings or money market\n\n"
        
        response += "**2. Debt Management:**\n"
        response += "• Pay off high-interest debt first (credit cards)\n"
        response += "• Consider debt consolidation if beneficial\n"
        response += "• Maintain good credit score (720+)\n\n"
        
        response += "**3. Investment Priorities:**\n"
        response += "• Maximize employer 401(k) match\n"
        response += "• Max out IRA contributions ($6,500/year, $7,500 if 50+)\n"
        response += "• Consider Roth vs Traditional based on tax situation\n"
        response += "• Taxable accounts for additional savings\n\n"
        
        response += "**4. Insurance Protection:**\n"
        response += "• Health insurance (essential)\n"
        response += "• Life insurance (10x annual income if dependents)\n"
        response += "• Disability insurance (protect income)\n"
        response += "• Property insurance (home/auto)\n\n"
        
        response += "**5. Tax Optimization:**\n"
        response += "• Tax-loss harvesting in taxable accounts\n"
        response += "• Asset location (bonds in tax-advantaged accounts)\n"
        response += "• Consider tax-efficient index funds\n"
        
        return response
    
    def _handle_equity_analysis_query(self, query: str, context: Dict = None) -> str:
        """Handle individual stock/company analysis queries"""
        response = "🏢 **Equity Analysis by Midas**\n\n"
        
        # Extract company/ticker if mentioned
        company = self._extract_company_mention(query)
        
        if company:
            response += f"**Analysis Framework for {company}:**\n\n"
        else:
            response += "**General Equity Analysis Framework:**\n\n"
        
        response += "**Fundamental Analysis Checklist:**\n"
        response += "• Revenue growth (5-year trend)\n"
        response += "• Profit margins (gross, operating, net)\n"
        response += "• Return on equity (ROE)\n"
        response += "• Debt-to-equity ratio\n"
        response += "• Free cash flow generation\n\n"
        
        response += "**Valuation Metrics:**\n"
        response += "• Price-to-Earnings (P/E) ratio\n"
        response += "• Price-to-Sales (P/S) ratio\n"
        response += "• Enterprise Value to EBITDA\n"
        response += "• Price-to-Book (P/B) ratio\n"
        response += "• PEG ratio (P/E to growth)\n\n"
        
        response += "**Qualitative Factors:**\n"
        response += "• Management quality and track record\n"
        response += "• Competitive moat and market position\n"
        response += "• Industry trends and disruption risks\n"
        response += "• Regulatory environment\n"
        response += "• ESG (Environmental, Social, Governance) factors\n\n"
        
        response += "💡 **Investment Approach:** Combine quantitative metrics with qualitative assessment. "
        response += "Consider the company within broader portfolio context."
        
        return response
    
    def _handle_crypto_query(self, query: str, context: Dict = None) -> str:
        """Handle cryptocurrency-related queries"""
        response = "₿ **Cryptocurrency Analysis by Midas**\n\n"
        
        response += "**Crypto Investment Considerations:**\n\n"
        
        response += "**Risk Assessment:**\n"
        response += "• Extremely volatile asset class\n"
        response += "• Regulatory uncertainty\n"
        response += "• Limited historical data\n"
        response += "• Technology and security risks\n"
        response += "• Liquidity concerns for smaller coins\n\n"
        
        response += "**Portfolio Allocation Guidance:**\n"
        response += "• Conservative: 1-3% of portfolio\n"
        response += "• Moderate: 3-7% of portfolio\n"
        response += "• Aggressive: 7-15% of portfolio\n"
        response += "• Never exceed what you can afford to lose\n\n"
        
        response += "**Major Cryptocurrencies Analysis:**\n"
        response += "• **Bitcoin (BTC):** Digital gold, store of value narrative\n"
        response += "• **Ethereum (ETH):** Smart contract platform, DeFi ecosystem\n"
        response += "• **Others:** Higher risk, potential for higher returns\n\n"
        
        response += "**Investment Strategies:**\n"
        response += "• Dollar-cost averaging to manage volatility\n"
        response += "• Focus on established cryptocurrencies\n"
        response += "• Use reputable exchanges with insurance\n"
        response += "• Consider crypto ETFs for easier access\n"
        response += "• Hardware wallet for security\n\n"
        
        response += "⚠️ **Crypto Warning:** Cryptocurrencies are speculative investments. "
        response += "Only invest money you can afford to lose completely."
        
        return response
    
    def _handle_general_financial_query(self, query: str, context: Dict = None) -> str:
        """Handle general financial queries"""
        response = "💰 **General Financial Guidance by Midas**\n\n"
        
        # Provide comprehensive financial wisdom
        response += "**Core Financial Principles:**\n\n"
        
        response += "**1. Pay Yourself First:**\n"
        response += "• Automate savings (10-20% of income)\n"
        response += "• Invest consistently regardless of market conditions\n"
        response += "• Increase savings rate with income growth\n\n"
        
        response += "**2. Time is Your Greatest Asset:**\n"
        response += "• Compound interest works best over long periods\n"
        response += "• Start investing early, even small amounts\n"
        response += "• Don't try to time the market\n\n"
        
        response += "**3. Diversification Reduces Risk:**\n"
        response += "• Don't put all eggs in one basket\n"
        response += "• Diversify across asset classes, sectors, geographies\n"
        response += "• Rebalance periodically\n\n"
        
        response += "**4. Control What You Can:**\n"
        response += "• Keep investment costs low (expense ratios)\n"
        response += "• Minimize taxes through tax-advantaged accounts\n"
        response += "• Stay disciplined during market volatility\n\n"
        
        response += "**5. Continuous Learning:**\n"
        response += "• Stay informed about market trends\n"
        response += "• Understand what you invest in\n"
        response += "• Regularly review and adjust strategy\n"
        
        return response
    
    def get_specialized_capabilities(self) -> List[str]:
        """Return Midas's specialized financial capabilities"""
        return [
            "Portfolio Analysis & Optimization",
            "Investment Research & Due Diligence", 
            "Risk Assessment & Management",
            "Financial Planning & Budgeting",
            "Market Analysis & Forecasting",
            "Equity Valuation & Analysis",
            "Fixed Income Strategy",
            "Alternative Investment Analysis",
            "Retirement Planning",
            "Tax-Efficient Investing",
            "Cryptocurrency Assessment",
            "Economic Model Building",
            "Financial Education & Literacy"
        ]
    
    def _initialize_market_knowledge(self) -> Dict:
        """Initialize market knowledge base"""
        return {
            'asset_classes': {
                'equities': {'risk': 'high', 'return_potential': 'high', 'liquidity': 'high'},
                'bonds': {'risk': 'low-medium', 'return_potential': 'low-medium', 'liquidity': 'medium-high'},
                'real_estate': {'risk': 'medium', 'return_potential': 'medium', 'liquidity': 'low'},
                'commodities': {'risk': 'high', 'return_potential': 'medium', 'liquidity': 'medium'},
                'crypto': {'risk': 'very_high', 'return_potential': 'very_high', 'liquidity': 'medium'}
            },
            'economic_indicators': [
                'GDP growth', 'inflation rate', 'unemployment rate', 'interest rates',
                'consumer confidence', 'housing data', 'manufacturing PMI'
            ],
            'market_cycles': ['accumulation', 'mark_up', 'distribution', 'mark_down']
        }
    
    def _initialize_risk_models(self) -> Dict:
        """Initialize risk assessment models"""
        return {
            'risk_tolerance_factors': [
                'age', 'income_stability', 'investment_experience', 
                'time_horizon', 'financial_goals', 'emotional_tolerance'
            ],
            'risk_metrics': [
                'standard_deviation', 'beta', 'sharpe_ratio', 'sortino_ratio',
                'maximum_drawdown', 'value_at_risk', 'correlation'
            ]
        }
    
    def _initialize_investment_strategies(self) -> Dict:
        """Initialize investment strategy frameworks"""
        return {
            'passive_strategies': [
                'index_investing', 'buy_and_hold', 'dollar_cost_averaging',
                'target_date_funds', 'asset_allocation_rebalancing'
            ],
            'active_strategies': [
                'value_investing', 'growth_investing', 'momentum_investing',
                'sector_rotation', 'market_timing', 'factor_investing'
            ],
            'alternative_strategies': [
                'hedge_funds', 'private_equity', 'real_estate_investment',
                'commodities_trading', 'cryptocurrency_investment'
            ]
        }
    
    def _initialize_financial_tools(self) -> Dict:
        """Initialize financial calculation tools"""
        return {
            'calculators': [
                'compound_interest', 'retirement_planning', 'loan_amortization',
                'present_value', 'future_value', 'portfolio_optimization'
            ],
            'analysis_tools': [
                'monte_carlo_simulation', 'scenario_analysis', 'sensitivity_analysis',
                'correlation_analysis', 'regression_analysis'
            ]
        }
    
    def _extract_portfolio_data(self, query: str) -> Optional[Dict]:
        """Extract portfolio information from query"""
        # Simple pattern matching - would be more sophisticated in full implementation
        portfolio_patterns = {
            'stock_percentage': r'(\d+)%?\s*(?:stocks?|equities)',
            'bond_percentage': r'(\d+)%?\s*bonds?',
            'cash_percentage': r'(\d+)%?\s*cash',
            'total_amount': r'\$?(\d+(?:,\d{3})*(?:\.\d{2})?)'
        }
        
        extracted_data = {}
        for key, pattern in portfolio_patterns.items():
            match = re.search(pattern, query.lower())
            if match:
                extracted_data[key] = match.group(1)
        
        return extracted_data if extracted_data else None
    
    def _analyze_existing_portfolio(self, portfolio_data: Dict) -> str:
        """Analyze provided portfolio data"""
        analysis = "**Current Portfolio Analysis:**\n"
        
        if 'stock_percentage' in portfolio_data:
            stock_pct = int(portfolio_data['stock_percentage'])
            analysis += f"• Equity allocation: {stock_pct}%\n"
            
            if stock_pct > 80:
                analysis += "  ⚠️ High equity concentration - consider diversification\n"
            elif stock_pct < 40:
                analysis += "  💡 Conservative allocation - may limit growth potential\n"
            else:
                analysis += "  ✅ Reasonable equity allocation for most investors\n"
        
        if 'bond_percentage' in portfolio_data:
            bond_pct = int(portfolio_data['bond_percentage'])
            analysis += f"• Fixed income allocation: {bond_pct}%\n"
        
        if 'total_amount' in portfolio_data:
            amount = portfolio_data['total_amount']
            analysis += f"• Portfolio value: ${amount}\n"
        
        return analysis
    
    def _provide_portfolio_guidance(self, query: str) -> str:
        """Provide general portfolio guidance"""
        guidance = "**Portfolio Construction Guidance:**\n\n"
        
        guidance += "**Age-Based Asset Allocation Rule of Thumb:**\n"
        guidance += "• Stock allocation = 110 - your age\n"
        guidance += "• Example: 30 years old → 80% stocks, 20% bonds\n"
        guidance += "• Adjust based on risk tolerance and goals\n\n"
        
        guidance += "**Core Portfolio Building Blocks:**\n"
        guidance += "• **Core Holdings (60-80%):** Low-cost index funds\n"
        guidance += "• **Satellite Holdings (10-20%):** Sector/factor tilts\n"
        guidance += "• **Alternative Assets (5-15%):** REITs, commodities, crypto\n"
        guidance += "• **Cash/Bonds:** Safety and opportunity fund\n\n"
        
        guidance += "**Diversification Dimensions:**\n"
        guidance += "• Asset classes (stocks, bonds, alternatives)\n"
        guidance += "• Geographic regions (US, international, emerging)\n"
        guidance += "• Sectors (technology, healthcare, finance, etc.)\n"
        guidance += "• Company sizes (large, mid, small cap)\n"
        guidance += "• Investment styles (value, growth, blend)\n"
        
        return guidance
    
    def _assess_portfolio_risk(self, query: str, portfolio_data: Dict = None) -> str:
        """Assess portfolio risk factors"""
        risk_assessment = "• **Concentration Risk:** Avoid over-weighting single stocks or sectors\n"
        risk_assessment += "• **Market Risk:** All investments subject to market volatility\n"
        risk_assessment += "• **Inflation Risk:** Fixed income vulnerable to inflation\n"
        risk_assessment += "• **Currency Risk:** International investments affected by exchange rates\n"
        risk_assessment += "• **Liquidity Risk:** Some investments harder to sell quickly\n"
        risk_assessment += "• **Interest Rate Risk:** Bond prices move opposite to rates\n\n"
        
        risk_assessment += "**Risk Mitigation Strategies:**\n"
        risk_assessment += "• Regular rebalancing (quarterly or semi-annually)\n"
        risk_assessment += "• Dollar-cost averaging for new investments\n"
        risk_assessment += "• Maintaining emergency fund outside investments\n"
        risk_assessment += "• Avoid emotional decision-making during volatility\n"
        
        return risk_assessment
    
    def _assess_risk_tolerance(self, query: str) -> Dict:
        """Assess risk tolerance from query content"""
        query_lower = query.lower()
        
        conservative_indicators = ['safe', 'conservative', 'low risk', 'stable', 'guaranteed']
        aggressive_indicators = ['growth', 'aggressive', 'high return', 'willing to risk']
        
        if any(indicator in query_lower for indicator in conservative_indicators):
            return {'level': 'conservative', 'capacity': 'Low volatility tolerance'}
        elif any(indicator in query_lower for indicator in aggressive_indicators):
            return {'level': 'aggressive', 'capacity': 'High volatility tolerance'}
        else:
            return {'level': 'moderate', 'capacity': 'Moderate volatility tolerance'}
    
    def _identify_market_focus(self, query: str) -> str:
        """Identify market focus from query"""
        query_lower = query.lower()
        
        if 'tech' in query_lower or 'technology' in query_lower:
            return "Technology Sector"
        elif 'real estate' in query_lower or 'reit' in query_lower:
            return "Real Estate Market"
        elif 'international' in query_lower or 'global' in query_lower:
            return "International Markets"
        elif 'small cap' in query_lower or 'small company' in query_lower:
            return "Small Cap Equities"
        else:
            return "General Market Analysis"
    
    def _extract_financial_goals(self, query: str) -> List[str]:
        """Extract financial goals mentioned in query"""
        goals = []
        query_lower = query.lower()
        
        goal_patterns = {
            'retirement': ['retire', 'retirement', '401k', 'ira'],
            'house_purchase': ['house', 'home', 'mortgage', 'down payment'],
            'education': ['college', 'education', 'tuition', '529'],
            'emergency_fund': ['emergency', 'emergency fund', 'safety net'],
            'debt_payoff': ['debt', 'pay off', 'credit card', 'loan']
        }
        
        for goal, keywords in goal_patterns.items():
            if any(keyword in query_lower for keyword in keywords):
                goals.append(goal.replace('_', ' ').title())
        
        return goals
    
    def _extract_company_mention(self, query: str) -> Optional[str]:
        """Extract company or ticker mention from query"""
        # Simple pattern matching for common stock patterns
        ticker_pattern = r'\b[A-Z]{1,5}\b'
        company_pattern = r'\b(?:Apple|Microsoft|Google|Amazon|Tesla|Netflix|Meta)\b'
        
        ticker_match = re.search(ticker_pattern, query)
        company_match = re.search(company_pattern, query, re.IGNORECASE)
        
        if company_match:
            return company_match.group()
        elif ticker_match and len(ticker_match.group()) <= 4:
            return ticker_match.group()
        
        return None
    
    def _get_specialization_keywords(self) -> List[str]:
        """Get keywords relevant to financial specialization"""
        return [
            'financial', 'investment', 'portfolio', 'stock', 'bond', 'fund',
            'money', 'finance', 'market', 'trading', 'economy', 'economic',
            'budget', 'save', 'saving', 'retirement', 'risk', 'return',
            'diversify', 'asset', 'allocation', 'valuation', 'analysis'
        ]

# Test the agent
if __name__ == "__main__":
    print("🧪 Testing Midas Financial Agent")
    print("="*50)
    
    midas = MidasAgent()
    
    print("\n💰 Agent Status:")
    status = midas.get_agent_status()
    for key, value in status.items():
        if key != 'specialized_capabilities':
            print(f"   {key}: {value}")
    
    print(f"\n🎯 Specialized Capabilities ({len(status['specialized_capabilities'])}):")
    for capability in status['specialized_capabilities']:
        print(f"   • {capability}")
    
    print("\n💼 Testing Financial Queries:")
    
    test_queries = [
        "I have $50,000 to invest. What should I do?",
        "How should I allocate my portfolio at age 35?",
        "Is Bitcoin a good investment?",
        "I want to retire in 20 years. How much should I save?",
        "What's the difference between stocks and bonds?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Test Query {i} ---")
        print(f"Query: {query}")
        response = midas.respond(query)
        print(f"Response Preview: {response[:200]}...")
    
    print(f"\n📊 Updated Status:")
    final_status = midas.get_agent_status()
    print(f"   Interactions: {final_status['interaction_count']}")
    print(f"   Expertise Level: {final_status['expertise_level']}")
    print(f"   Memory Count: {final_status['memory_count']}")
    
    print("\n✅ Midas agent test complete!")
