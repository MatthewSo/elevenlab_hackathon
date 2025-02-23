from backend.llm.mistral_statement_evaluator import MistralStatementEvaluator
from backend.voice.elevenlabs_speech_generator import ElevenLabsSpeechGenerator

mistral_eval = MistralStatementEvaluator('''ElevenLabs x a16z WW Hackathon (in-person)
Congratulations, you’re in. You are among the top few who have secured a spot out of the hundreds of applications we received.

Locations: London, New York, San Francisco, Warsaw, Bengaluru & Seoul
Date: February 22–23, 2025
Overview

ElevenLabs and a16z are holding a worldwide hackathon focused on AI AGENTS.
We will be hosting 7 hackathons simultaneously over one weekend, bringing together the world's best builders, tinkerers, designers and AI engineers.
Important - Event Discord access
You will have received a text with an invitation to Discord, you must join this as soon as possible to confirm your attendance at each location.
1. Join the ElevenLabs discord: https://discord.gg/elevenlabs
2. Join/locate the #hackathon-announcements channel
3. Read the announcement carefully & click on your respective location
4. You will then be added to the relevant Discord channel, for example #ww-san-francisco. Where you will be able to meet other participants before the event.
Prizes
Main ElevenLabs prize track (AI agents)
Criteria: Use of ElevenLabs to build AI agents

                                        - Global top prize: Teenage Engineering TP-7 (per team member)
- 1st Prize: Mac Mini M4s (per team member)
- 2nd Prize: Teenage Engineering OB-4 (per team member)
- 3rd Prize: Shure MV6s (per team member)
Global Prize: One winning team will be selected globally to receive the Global Top Prize.
Sponsor prize tracks
Global fal Prize track ($24,000 in credits) - 1 winning team globally
Criteria: Best use case of generative media models via fal API during the event for a chance to win up to $24,000 in fal credits.

Global Posthog Prize track ($22,000 in credits) - 1 winning team globally
Criteria: Build with the PostHog LLM observability tool during the event to be in for a chance to win $22,000 PostHog credits.

Global Lovable Prize track: 1 year Lovable subscription for the entire team
Criteria: Build an awesome app using Lovable and submit Lovable project link
Other prizes
Vercel: $300 off Vercel for 6 months



Theme

AI Agents
You will build AI Agents using ElevenLabs & partner models/tools.
Your project may incorporate one of the partner technologies from: PostHog, Lovable, Clerk, Make, PICA, fal.ai, Vercel and/or Mistral.

All projects must be built from scratch. Pre-existing or prepared projects are not allowed. You may use templates.
Criteria

Impact (25% weight)
What is the project’s potential for long-term success, scalability, and societal impact?
Technical Implementation (25% weight)
How well has the team implemented the idea?
Does the technical implementation have the potential to support the proposed solution?
Creativity and Innovation (25% weight)
Is the project’s concept innovative, unique, and creative?
Pitch and Presentation (25% weight)
How effectively does the team present and articulate their project, its value proposition, and its potential impact?
Global judges


Rules

The submission must be created entirely from scratch during the time permitted, leveraging only widely available open-source technologies and publicly available APIs. Any attempt to use prior work will result in immediate disqualification.
You must follow this code of conduct at all times.
In-person teams must be composed of a minimum of 2 & maximum 4 people.
Participants will have time for team formation on the first day of the event, as well as Discord communication channels for discussion and team finding days in advance.
Submission & judging

All teams must submit their project to Devpost by the time provided at each venue: https://elevenlabs-worldwide-hackathon.devpost.com
All project submissions must include:
Video: A publicly accessible demo video showcasing key features (max 2 minutes)
Project overview: Title & summary of the problem/solution
Team information: List all members with roles/contributions
Technical details: Tech stack, public repository link + visuals (screenshots or diagrams)
Compliance: Acknowledge adherence to hackathon rules and deadlines.
The hackathon will employ a two-round judging process:
First Round: Projects will be narrowed down to the top six entries.
Judging conducted in multiple rooms with 2-3 judges per room.
Scores will be internally moderated for fairness.
Final Round: High-profile judges will evaluate the top 6 projects.''')

test = input("statement:")
evaluation = mistral_eval.evaluate_statement(test)
print(evaluation)

explanation = mistral_eval.generate_explanation(test, evaluation)
print(explanation)

speech_generator = ElevenLabsSpeechGenerator()

speech_generator.generate_speech(explanation)