/* DevSnips Job Board — script.js
   Application logic: views, job/company/candidate rendering,
   search + filters + pagination, save/apply, mobile nav + filter drawer.
   Vanilla JS, no dependencies. Loaded at end of <body> so the DOM is ready. */
(function() {
            // ── Application Data ──────────────────
            const companies = [
                { id: 'vercel', name: 'Vercel', logo: 'V', desc: 'Build, deploy, and scale modern web applications with the frontend cloud platform.', website: 'vercel.com',
                    location: 'San Francisco, CA', size: '200-500', industry: 'Cloud Infrastructure', openPositions: 12,
                    overview: 'Vercel provides the developer tools and cloud infrastructure to build, scale, and secure a faster, more personalized web. Their platform enables frontend teams to do their best work.' },
                { id: 'linear', name: 'Linear', logo: 'L', desc: 'A streamlined issue tracking and project management tool built for speed.', website: 'linear.app',
                    location: 'San Francisco, CA', size: '50-200', industry: 'Developer Tools', openPositions: 6,
                    overview: 'Linear is redefining how software teams build products. Purpose-built for planning and building great software, Linear helps teams streamline issues, sprints, and product roadmaps.' },
                { id: 'stripe', name: 'Stripe', logo: 'S', desc: 'Financial infrastructure platform for businesses of all sizes.', website: 'stripe.com',
                    location: 'San Francisco, CA', size: '5,000+', industry: 'Fintech', openPositions: 45,
                    overview: 'Stripe builds economic infrastructure for the internet. Businesses of every size use Stripe to accept payments, send payouts, and manage their businesses online.' },
                { id: 'figma', name: 'Figma', logo: 'F', desc: 'Collaborative interface design tool powering product teams worldwide.', website: 'figma.com',
                    location: 'San Francisco, CA', size: '1,000-2,000', industry: 'Design Tools', openPositions: 18,
                    overview: 'Figma is the leading collaborative design tool for building meaningful products. Seamlessly design, prototype, develop, and collect feedback in a single platform.' },
                { id: 'notion', name: 'Notion', logo: 'N', desc: 'All-in-one workspace for notes, docs, wikis, and project management.', website: 'notion.so',
                    location: 'San Francisco, CA', size: '500-1,000', industry: 'Productivity', openPositions: 14,
                    overview: 'Notion is a single space where you can think, write, and plan. Capture thoughts, manage projects, or even run an entire company — and do it exactly the way you want.' },
                { id: 'supabase', name: 'Supabase', logo: 'Sb', desc: 'Open source Firebase alternative providing instant backend infrastructure.', website: 'supabase.com',
                    location: 'Remote', size: '50-200', industry: 'Developer Tools', openPositions: 9,
                    overview: 'Supabase is an open source Firebase alternative. Start your project with a Postgres database, Authentication, instant APIs, Edge Functions, Realtime subscriptions, and Storage.' },
                { id: 'railway', name: 'Railway', logo: 'R', desc: 'Infrastructure platform that makes deploying services simple and fast.', website: 'railway.app',
                    location: 'Remote', size: '20-50', industry: 'Cloud Infrastructure', openPositions: 4,
                    overview: 'Railway is an infrastructure platform where you can provision infrastructure, develop with that infrastructure locally, and then deploy to the cloud.' },
                { id: 'clerk', name: 'Clerk', logo: 'C', desc: 'Complete user management and authentication for modern applications.', website: 'clerk.com',
                    location: 'San Francisco, CA', size: '20-50', industry: 'Developer Tools', openPositions: 3,
                    overview: 'Clerk provides drop-in authentication and user management for modern web applications. Embed complete user management UIs and APIs in minutes.' },
                { id: 'resend', name: 'Resend', logo: 'Re', desc: 'Modern email API for developers to build, test, and send emails.', website: 'resend.com',
                    location: 'San Francisco, CA', size: '10-30', industry: 'Developer Tools', openPositions: 2,
                    overview: 'Resend is the email API for developers. Build, test, and send transactional emails at scale with a modern, developer-friendly platform.' },
                { id: 'render', name: 'Render', logo: 'Rd', desc: 'Unified cloud platform to build and run all your apps and websites.', website: 'render.com',
                    location: 'San Francisco, CA', size: '100-300', industry: 'Cloud Infrastructure', openPositions: 8,
                    overview: 'Render is a unified cloud to build and run all your apps and websites with free TLS certificates, a global CDN, DDoS protection, private networks, and auto deploys from Git.' },
            ];

            const jobs = [
                { id: 1, title: 'Senior Frontend Developer', company: 'Vercel', companyId: 'vercel', location: 'San Francisco, CA',
                    salary: '$160,000 – $210,000', workMode: 'Hybrid', type: 'full-time', experience: 'Senior',
                    posted: '2 days ago', skills: ['React', 'Next.js', 'TypeScript', 'Tailwind CSS', 'GraphQL'],
                    description: 'Join the team building the frontend cloud. You\'ll work on developer-facing products that millions of developers use daily to deploy and scale their web applications. Help shape the future of frontend infrastructure with a team that values craft, performance, and developer experience above all.',
                    responsibilities: [
                        'Architect and build high-performance React applications used by millions of developers',
                        'Collaborate with design and product teams to ship polished, accessible user interfaces',
                        'Improve build tooling, CI/CD pipelines, and developer workflows',
                        'Mentor junior engineers and contribute to technical design discussions',
                        'Write clean, tested, and well-documented code'
                    ],
                    requirements: [
                        '5+ years of experience in frontend development with React and TypeScript',
                        'Deep understanding of web performance optimization and Core Web Vitals',
                        'Experience with Next.js and server-side rendering patterns',
                        'Strong eye for design and attention to detail',
                        'Excellent communication skills and a collaborative mindset'
                    ],
                    benefits: ['Competitive salary and equity', 'Flexible PTO', 'Health, dental, and vision',
                        'Home office stipend', 'Learning and development budget'
                    ] },
                { id: 2, title: 'Backend Engineer', company: 'Stripe', companyId: 'stripe', location: 'New York, NY',
                    salary: '$170,000 – $230,000', workMode: 'On-site', type: 'full-time', experience: 'Mid-Senior',
                    posted: '1 week ago', skills: ['Java', 'Ruby', 'Distributed Systems', 'PostgreSQL', 'gRPC'],
                    description: 'Build the core payment processing infrastructure that powers millions of businesses globally. You\'ll design and implement highly reliable distributed systems that handle billions of dollars in transactions while maintaining sub-millisecond latency.',
                    responsibilities: [
                        'Design and build scalable, fault-tolerant distributed systems',
                        'Optimize database queries and API performance for high-throughput scenarios',
                        'Participate in on-call rotations and incident response',
                        'Write comprehensive tests and contribute to code review culture',
                        'Collaborate across teams to define API contracts and service boundaries'
                    ],
                    requirements: [
                        '4+ years of backend engineering experience',
                        'Strong proficiency in at least one of: Java, Ruby, Go, or Rust',
                        'Experience with distributed systems and microservices architecture',
                        'Knowledge of database internals and query optimization',
                        'Track record of shipping reliable production systems'
                    ],
                    benefits: ['Top-tier compensation', 'Comprehensive healthcare', '401(k) matching',
                        'Wellness stipend', 'Relocation assistance'
                    ] },
                { id: 3, title: 'Product Designer', company: 'Figma', companyId: 'figma', location: 'San Francisco, CA',
                    salary: '$150,000 – $200,000', workMode: 'Hybrid', type: 'full-time', experience: 'Senior',
                    posted: '3 days ago', skills: ['UI Design', 'Design Systems', 'Prototyping', 'Figma', 'User Research'],
                    description: 'Shape the future of collaborative design tools. As a product designer at Figma, you\'ll craft intuitive, powerful experiences that empower designers and developers to create their best work together.',
                    responsibilities: [
                        'Lead design projects from concept through implementation',
                        'Conduct user research and translate insights into design decisions',
                        'Create high-fidelity prototypes and detailed interaction specifications',
                        'Contribute to and evolve Figma\'s design system',
                        'Partner with engineering to ensure pixel-perfect implementation'
                    ],
                    requirements: [
                        '5+ years of product design experience',
                        'Exceptional portfolio demonstrating complex problem-solving',
                        'Deep expertise with Figma and modern design tools',
                        'Experience contributing to or maintaining design systems',
                        'Strong communication and storytelling skills'
                    ],
                    benefits: ['Competitive compensation', 'Equity package', 'Health coverage', '401(k)',
                        'Annual design conference budget'
                    ] },
                { id: 4, title: 'DevOps Engineer', company: 'Railway', companyId: 'railway', location: 'Remote',
                    salary: '$140,000 – $185,000', workMode: 'Remote', type: 'full-time', experience: 'Mid-Senior',
                    posted: '5 days ago', skills: ['Kubernetes', 'Terraform', 'AWS', 'Docker', 'CI/CD', 'Go'],
                    description: 'Build the infrastructure platform that lets developers deploy applications with a single command. You\'ll work on container orchestration, networking, and deployment automation at scale.',
                    responsibilities: [
                        'Design and maintain Kubernetes clusters and container orchestration systems',
                        'Build internal tooling for infrastructure provisioning and monitoring',
                        'Improve deployment pipelines and reduce build times',
                        'Implement security best practices across cloud infrastructure',
                        'Document infrastructure patterns and mentor team members'
                    ],
                    requirements: [
                        '4+ years of experience in DevOps or platform engineering',
                        'Deep knowledge of Kubernetes and container ecosystems',
                        'Experience with infrastructure-as-code using Terraform or Pulumi',
                        'Strong programming skills in Go, Python, or similar',
                        'Passion for developer experience and automation'
                    ],
                    benefits: ['Fully remote', 'Competitive salary', 'Flexible hours', 'Equipment budget',
                        'Annual team retreats'
                    ] },
                { id: 5, title: 'Full Stack Developer', company: 'Notion', companyId: 'notion', location: 'San Francisco, CA',
                    salary: '$155,000 – $205,000', workMode: 'Hybrid', type: 'full-time', experience: 'Mid-Senior',
                    posted: '1 day ago', skills: ['React', 'TypeScript', 'Node.js', 'PostgreSQL', 'Redis'],
                    description: 'Build features that help millions of people organize their work and life. You\'ll work across the full stack, from the React frontend to the distributed backend that powers real-time collaboration.',
                    responsibilities: [
                        'Develop and ship features across the entire stack',
                        'Optimize real-time collaboration performance and reliability',
                        'Build reusable UI components that scale across platforms',
                        'Participate in technical design and architecture reviews',
                        'Contribute to a culture of engineering excellence'
                    ],
                    requirements: [
                        '4+ years of full stack development experience',
                        'Proficiency with React, TypeScript, and Node.js',
                        'Experience with relational databases and caching strategies',
                        'Understanding of real-time systems and WebSocket protocols',
                        'Product-minded with a focus on user experience'
                    ],
                    benefits: ['Competitive salary', 'Equity', 'Health benefits', 'Unlimited PTO',
                        'Learning stipend'
                    ] },
                { id: 6, title: 'Data Engineer', company: 'Supabase', companyId: 'supabase', location: 'Remote',
                    salary: '$135,000 – $175,000', workMode: 'Remote', type: 'full-time', experience: 'Mid',
                    posted: '4 days ago', skills: ['PostgreSQL', 'Python', 'Apache Spark', 'dbt', 'Airflow',
                        'Data Modeling'],
                    description: 'Build the data infrastructure that powers Supabase\'s analytics and observability platforms. Design data pipelines, optimize query performance, and create tools that help developers understand their data.',
                    responsibilities: [
                        'Design and maintain scalable ETL pipelines and data warehouses',
                        'Optimize PostgreSQL query performance and schema design',
                        'Build data models and dashboards for internal analytics',
                        'Create tooling for data quality monitoring and alerting',
                        'Collaborate with product teams on data-driven features'
                    ],
                    requirements: [
                        '3+ years of data engineering experience',
                        'Expert-level PostgreSQL knowledge',
                        'Experience with workflow orchestration tools like Airflow',
                        'Proficiency in Python and SQL',
                        'Strong analytical and problem-solving skills'
                    ],
                    benefits: ['Fully remote', 'Open source contribution time', 'Competitive pay', 'Flexible schedule',
                        'Conference budget'
                    ] },
                { id: 7, title: 'Frontend Developer', company: 'Linear', companyId: 'linear', location: 'San Francisco, CA',
                    salary: '$145,000 – $190,000', workMode: 'Hybrid', type: 'full-time', experience: 'Mid',
                    posted: '6 days ago', skills: ['React', 'TypeScript', 'CSS', 'GraphQL', 'Jest'],
                    description: 'Craft pixel-perfect interfaces for a project management tool that developers love. At Linear, quality is paramount — you\'ll build interfaces that are fast, accessible, and delightful to use.',
                    responsibilities: [
                        'Build and maintain high-quality React components with TypeScript',
                        'Optimize rendering performance and reduce bundle size',
                        'Implement complex animations and micro-interactions',
                        'Write comprehensive unit and integration tests',
                        'Collaborate closely with designers on interaction patterns'
                    ],
                    requirements: [
                        '3+ years of frontend development experience',
                        'Strong TypeScript and React skills',
                        'Deep understanding of CSS, layout, and responsive design',
                        'Experience with GraphQL APIs',
                        'Obsession with details and polish'
                    ],
                    benefits: ['Top salary', 'Meaningful equity', 'Health coverage', 'Flexible PTO',
                        'Office in downtown SF'
                    ] },
                { id: 8, title: 'Security Engineer', company: 'Clerk', companyId: 'clerk', location: 'San Francisco, CA',
                    salary: '$165,000 – $215,000', workMode: 'Hybrid', type: 'full-time', experience: 'Senior',
                    posted: '1 week ago', skills: ['OAuth', 'OIDC', 'Cryptography', 'Web Security', 'Go', 'TypeScript'],
                    description: 'Help build the most secure authentication platform for modern applications. You\'ll design and implement security protocols, conduct audits, and ensure Clerk remains a trusted foundation for thousands of apps.',
                    responsibilities: [
                        'Design and implement authentication and authorization protocols',
                        'Conduct security audits and penetration testing',
                        'Develop security monitoring and incident response systems',
                        'Stay current with emerging threats and vulnerabilities',
                        'Advise engineering teams on security best practices'
                    ],
                    requirements: [
                        '5+ years of security engineering experience',
                        'Deep knowledge of OAuth 2.0, OIDC, and SAML protocols',
                        'Experience with cryptographic primitives and their applications',
                        'Strong programming skills in Go or TypeScript',
                        'Track record of responsible vulnerability disclosure'
                    ],
                    benefits: ['Competitive salary', 'Equity', 'Health benefits', 'Security conference budget',
                        'Flexible working'
                    ] },
                { id: 9, title: 'Developer Advocate', company: 'Resend', companyId: 'resend', location: 'Remote',
                    salary: '$130,000 – $170,000', workMode: 'Remote', type: 'full-time', experience: 'Mid',
                    posted: '3 days ago', skills: ['Technical Writing', 'Public Speaking', 'Node.js', 'React',
                        'API Design'],
                    description: 'Be the voice of Resend in the developer community. Create content, give talks, and help developers build better email experiences. You\'ll bridge the gap between our engineering team and the broader developer ecosystem.',
                    responsibilities: [
                        'Create high-quality technical content including blog posts, tutorials, and videos',
                        'Speak at conferences and meetups about email infrastructure',
                        'Engage with the developer community on social media and forums',
                        'Gather developer feedback and advocate for product improvements',
                        'Build demo applications and integration examples'
                    ],
                    requirements: [
                        '3+ years of experience in developer relations or software engineering',
                        'Excellent written and verbal communication skills',
                        'Experience building with modern web technologies',
                        'Active presence in developer communities',
                        'Comfortable with public speaking and live coding'
                    ],
                    benefits: ['Fully remote', 'Competitive salary', 'Travel budget', 'Content creation budget',
                        'Flexible hours'
                    ] },
                { id: 10, title: 'Senior Backend Engineer', company: 'Render', companyId: 'render', location: 'San Francisco, CA',
                    salary: '$175,000 – $225,000', workMode: 'Hybrid', type: 'full-time', experience: 'Senior',
                    posted: '2 days ago', skills: ['Go', 'Kubernetes', 'PostgreSQL', 'Redis', 'gRPC', 'Distributed Systems'],
                    description: 'Design and build the core infrastructure that powers Render\'s cloud platform. You\'ll work on service orchestration, networking, and deployment systems that make cloud infrastructure simple for developers.',
                    responsibilities: [
                        'Architect and implement scalable backend services',
                        'Optimize service mesh and inter-service communication',
                        'Build internal APIs and developer-facing features',
                        'Mentor engineers and lead technical initiatives',
                        'Participate in architectural decision-making'
                    ],
                    requirements: [
                        '6+ years of backend engineering experience',
                        'Expert-level Go programming skills',
                        'Deep experience with Kubernetes and container orchestration',
                        'Strong understanding of distributed systems principles',
                        'Experience leading technical projects'
                    ],
                    benefits: ['Competitive compensation', 'Equity', 'Health insurance', 'Unlimited PTO',
                        'Remote-friendly'
                    ] },
                { id: 11, title: 'Frontend Platform Engineer', company: 'Vercel', companyId: 'vercel', location: 'London, UK',
                    salary: '£90,000 – £130,000', workMode: 'Hybrid', type: 'full-time', experience: 'Mid-Senior',
                    posted: '1 week ago', skills: ['Next.js', 'React', 'TypeScript', 'Edge Computing',
                    'Web Performance'],
                    description: 'Build the tools and frameworks that define modern frontend development. Work on Next.js and related open-source projects that power the web. You\'ll contribute to the ecosystem used by millions.',
                    responsibilities: [
                        'Contribute to Next.js and related open-source projects',
                        'Build developer tooling for frontend performance optimization',
                        'Write documentation and examples for the developer community',
                        'Collaborate with the React core team on framework features',
                        'Engage with the open-source community through issues and PRs'
                    ],
                    requirements: [
                        '4+ years of frontend development experience',
                        'Deep expertise with React and Next.js',
                        'Experience contributing to open-source projects',
                        'Strong understanding of web performance and edge computing',
                        'Excellent technical communication skills'
                    ],
                    benefits: ['Competitive salary', 'Equity', 'Health coverage', 'Open source contribution time',
                        'Conference budget'
                    ] },
                { id: 12, title: 'Product Manager', company: 'Linear', companyId: 'linear', location: 'San Francisco, CA',
                    salary: '$160,000 – $210,000', workMode: 'Hybrid', type: 'full-time', experience: 'Senior',
                    posted: '5 days ago', skills: ['Product Strategy', 'User Research', 'Analytics', 'Developer Tools',
                        'Agile'],
                    description: 'Drive the product vision for Linear\'s core project management experience. You\'ll work closely with engineering and design to ship features that delight developers and product teams.',
                    responsibilities: [
                        'Define product roadmap and prioritize features based on user impact',
                        'Conduct user research and analyze product metrics',
                        'Write detailed product specifications and acceptance criteria',
                        'Collaborate with engineering on technical feasibility',
                        'Communicate product decisions and rationale to stakeholders'
                    ],
                    requirements: [
                        '5+ years of product management experience',
                        'Experience with developer tools or productivity software',
                        'Strong analytical skills and data-driven decision-making',
                        'Excellent written and verbal communication',
                        'Technical background preferred'
                    ],
                    benefits: ['Top salary', 'Equity', 'Health benefits', 'Flexible PTO', 'Downtown SF office'] },
                { id: 13, title: 'iOS Developer', company: 'Figma', companyId: 'figma', location: 'New York, NY',
                    salary: '$155,000 – $200,000', workMode: 'Hybrid', type: 'full-time', experience: 'Mid-Senior',
                    posted: '4 days ago', skills: ['Swift', 'SwiftUI', 'UIKit', 'Core Animation', 'Metal'],
                    description: 'Build the Figma mobile experience that brings collaborative design to iOS. Create smooth, performant native applications that designers love to use on the go.',
                    responsibilities: [
                        'Develop and maintain the Figma iOS application',
                        'Optimize rendering performance for complex design files',
                        'Implement custom UI components and animations',
                        'Collaborate with design team on mobile interaction patterns',
                        'Write unit and UI tests to ensure quality'
                    ],
                    requirements: [
                        '4+ years of iOS development experience',
                        'Proficiency in Swift and SwiftUI',
                        'Experience with complex UI and custom drawing',
                        'Understanding of mobile performance optimization',
                        'Strong attention to detail and design sensibilities'
                    ],
                    benefits: ['Competitive salary', 'Equity', 'Health coverage', 'Device budget', '401(k)'] },
                { id: 14, title: 'Solutions Architect', company: 'Stripe', companyId: 'stripe', location: 'Amsterdam, NL',
                    salary: '€95,000 – €140,000', workMode: 'Hybrid', type: 'full-time', experience: 'Senior',
                    posted: '1 week ago', skills: ['API Design', 'System Architecture', 'Payments', 'Cloud', 'Technical Sales'],
                    description: 'Help Stripe\'s largest European customers integrate and optimize their payment infrastructure. You\'ll design solutions, lead technical discussions, and ensure successful implementations.',
                    responsibilities: [
                        'Design payment integration architectures for enterprise customers',
                        'Lead technical discovery sessions and solution design workshops',
                        'Create reference implementations and integration guides',
                        'Collaborate with product teams on customer requirements',
                        'Represent Stripe at industry events and conferences'
                    ],
                    requirements: [
                        '6+ years in solutions architecture or technical consulting',
                        'Deep understanding of API design and system integration',
                        'Experience with payment systems or financial technology',
                        'Excellent communication in English; additional European languages a plus',
                        'Willingness to travel within Europe'
                    ],
                    benefits: ['Competitive salary', 'Equity', 'Health benefits', 'Travel budget',
                        'Relocation support'
                    ] },
                { id: 15, title: 'Machine Learning Engineer', company: 'Notion', companyId: 'notion', location: 'San Francisco, CA',
                    salary: '$180,000 – $240,000', workMode: 'Hybrid', type: 'full-time', experience: 'Senior',
                    posted: '2 days ago', skills: ['Python', 'PyTorch', 'NLP', 'Transformers', 'MLOps', 'AWS'],
                    description: 'Build AI-powered features that make Notion smarter. Work on natural language processing, search relevance, and intelligent content understanding that helps users get more from their workspace.',
                    responsibilities: [
                        'Develop and deploy machine learning models for content understanding',
                        'Build and maintain ML infrastructure and training pipelines',
                        'Collaborate with product teams to identify AI opportunities',
                        'Optimize model inference for low-latency production serving',
                        'Stay current with advances in NLP and generative AI'
                    ],
                    requirements: [
                        '5+ years of machine learning experience',
                        'Strong programming skills in Python',
                        'Experience with PyTorch or TensorFlow',
                        'Knowledge of NLP and transformer architectures',
                        'Track record of deploying ML models to production'
                    ],
                    benefits: ['Top compensation', 'Equity', 'Health benefits', 'Research budget', 'Flexible working'] },
                { id: 16, title: 'Technical Writer', company: 'Supabase', companyId: 'supabase', location: 'Remote',
                    salary: '$100,000 – $140,000', workMode: 'Remote', type: 'full-time', experience: 'Mid',
                    posted: '6 days ago', skills: ['Technical Writing', 'SQL', 'REST APIs', 'Documentation', 'Markdown'],
                    description: 'Create world-class documentation that helps developers build with Supabase. Write guides, API references, and tutorials that make complex concepts accessible and actionable.',
                    responsibilities: [
                        'Write and maintain API documentation and developer guides',
                        'Create tutorials and quickstart guides for various frameworks',
                        'Review and improve existing documentation for clarity and accuracy',
                        'Collaborate with engineering on new feature documentation',
                        'Gather developer feedback to improve documentation quality'
                    ],
                    requirements: [
                        '3+ years of technical writing experience',
                        'Understanding of SQL and REST APIs',
                        'Excellent written English',
                        'Experience with documentation tools and static site generators',
                        'Ability to explain complex technical concepts clearly'
                    ],
                    benefits: ['Fully remote', 'Competitive salary', 'Flexible hours', 'Learning budget',
                        'Open source contribution'
                    ] },
                { id: 17, title: 'Platform Engineer', company: 'Railway', companyId: 'railway', location: 'Remote',
                    salary: '$150,000 – $195,000', workMode: 'Remote', type: 'full-time', experience: 'Mid-Senior',
                    posted: '3 days ago', skills: ['Go', 'Rust', 'Kubernetes', 'Linux', 'Networking', 'Nix'],
                    description: 'Build the core platform that makes deploying infrastructure as simple as writing code. Work on container runtimes, build systems, and deployment orchestration at the cutting edge.',
                    responsibilities: [
                        'Develop and maintain the container orchestration platform',
                        'Build and optimize build systems for various language ecosystems',
                        'Design networking and service discovery systems',
                        'Implement monitoring and observability infrastructure',
                        'Contribute to open-source projects in the platform ecosystem'
                    ],
                    requirements: [
                        '4+ years of platform or systems engineering experience',
                        'Strong programming skills in Go or Rust',
                        'Deep Linux systems knowledge',
                        'Experience with container runtimes and orchestration',
                        'Passion for developer tooling and infrastructure'
                    ],
                    benefits: ['Fully remote', 'Competitive salary', 'Equipment budget', 'Flexible PTO',
                        'Team retreats'
                    ] },
                { id: 18, title: 'UX Researcher', company: 'Figma', companyId: 'figma', location: 'San Francisco, CA',
                    salary: '$140,000 – $185,000', workMode: 'Hybrid', type: 'full-time', experience: 'Mid-Senior',
                    posted: '1 week ago', skills: ['User Research', 'Usability Testing', 'Data Analysis', 'Survey Design',
                        'Design Thinking'],
                    description: 'Conduct research that shapes the future of collaborative design. Understand how designers and developers work together and uncover insights that drive product strategy.',
                    responsibilities: [
                        'Plan and conduct qualitative and quantitative user research',
                        'Synthesize research findings into actionable insights',
                        'Collaborate with product and design teams on research priorities',
                        'Build research operations and participant recruitment systems',
                        'Present findings to stakeholders and leadership'
                    ],
                    requirements: [
                        '4+ years of UX research experience',
                        'Strong portfolio demonstrating research impact',
                        'Experience with both qualitative and quantitative methods',
                        'Excellent communication and storytelling skills',
                        'Background in HCI, psychology, or related field preferred'
                    ],
                    benefits: ['Competitive salary', 'Equity', 'Health coverage', 'Research budget', '401(k)'] },
                { id: 19, title: 'Site Reliability Engineer', company: 'Stripe', companyId: 'stripe', location: 'San Francisco, CA',
                    salary: '$175,000 – $235,000', workMode: 'Hybrid', type: 'full-time', experience: 'Senior',
                    posted: '4 days ago', skills: ['Go', 'Linux', 'Kubernetes', 'Prometheus', 'Terraform',
                        'Incident Response'],
                    description: 'Ensure Stripe\'s payment infrastructure maintains exceptional reliability at global scale. Design systems, automate operations, and lead incident response for mission-critical services.',
                    responsibilities: [
                        'Design and implement reliability improvements across services',
                        'Build automation to reduce operational toil',
                        'Lead incident response and post-incident reviews',
                        'Define and monitor SLOs and error budgets',
                        'Mentor engineering teams on reliability best practices'
                    ],
                    requirements: [
                        '5+ years of SRE or platform engineering experience',
                        'Strong programming skills, preferably in Go',
                        'Deep experience with observability and monitoring tools',
                        'Track record of improving system reliability at scale',
                        'Calm and effective during incidents'
                    ],
                    benefits: ['Top compensation', 'Equity', 'Health benefits', 'On-call compensation',
                        'Wellness program'
                    ] },
                { id: 20, title: 'Full Stack Developer', company: 'Clerk', companyId: 'clerk', location: 'Remote',
                    salary: '$130,000 – $170,000', workMode: 'Remote', type: 'full-time', experience: 'Mid',
                    posted: '2 days ago', skills: ['React', 'TypeScript', 'Node.js', 'PostgreSQL', 'OAuth'],
                    description: 'Build the user management platform that thousands of developers rely on. Work on both the frontend SDKs and backend APIs that make authentication simple and secure.',
                    responsibilities: [
                        'Develop and maintain React SDKs and UI components',
                        'Build robust backend APIs for user management',
                        'Write clear documentation and integration guides',
                        'Collaborate on API design and developer experience',
                        'Respond to community feedback and contribute to open source'
                    ],
                    requirements: [
                        '3+ years of full stack development experience',
                        'Proficiency with React, TypeScript, and Node.js',
                        'Experience with authentication and authorization patterns',
                        'Strong written communication skills',
                        'Passion for developer experience'
                    ],
                    benefits: ['Fully remote', 'Competitive salary', 'Equity', 'Health benefits', 'Flexible schedule'] },
                { id: 21, title: 'Growth Engineer', company: 'Notion', companyId: 'notion', location: 'New York, NY',
                    salary: '$150,000 – $200,000', workMode: 'Hybrid', type: 'full-time', experience: 'Mid-Senior',
                    posted: '5 days ago', skills: ['React', 'TypeScript', 'A/B Testing', 'Analytics', 'Growth Strategy'],
                    description: 'Drive user acquisition and engagement through data-informed product experiments. Build features that help more people discover and adopt Notion as their primary workspace.',
                    responsibilities: [
                        'Design and implement growth experiments across the product',
                        'Build A/B testing infrastructure and analyze experiment results',
                        'Optimize onboarding flows and activation funnels',
                        'Collaborate with marketing on product-led growth initiatives',
                        'Ship fast and iterate based on data'
                    ],
                    requirements: [
                        '4+ years of engineering experience with a growth focus',
                        'Strong React and TypeScript skills',
                        'Experience with A/B testing and experimentation platforms',
                        'Data-driven mindset with strong analytical skills',
                        'Entrepreneurial spirit and bias for action'
                    ],
                    benefits: ['Competitive salary', 'Equity', 'Health benefits', 'Unlimited PTO', 'NYC office'] },
                { id: 22, title: 'Developer Relations Engineer', company: 'Resend', companyId: 'resend', location: 'Remote',
                    salary: '$120,000 – $160,000', workMode: 'Remote', type: 'full-time', experience: 'Mid',
                    posted: '1 week ago', skills: ['Node.js', 'React', 'API Design', 'Technical Content',
                        'Community Building'],
                    description: 'Build and nurture the developer community around Resend. Create integrations, write content, and help developers succeed with email infrastructure.',
                    responsibilities: [
                        'Build SDK libraries and integration examples for popular frameworks',
                        'Write technical blog posts, tutorials, and documentation',
                        'Engage with developers on GitHub, Discord, and social media',
                        'Speak at conferences and host workshops',
                        'Gather and synthesize developer feedback for the product team'
                    ],
                    requirements: [
                        '3+ years in developer relations or software engineering',
                        'Strong JavaScript/TypeScript skills',
                        'Experience building and shipping side projects',
                        'Excellent communication and teaching skills',
                        'Active in developer communities'
                    ],
                    benefits: ['Fully remote', 'Competitive salary', 'Travel budget', 'Content budget',
                        'Flexible hours'
                    ] },
                { id: 23, title: 'Engineering Manager', company: 'Linear', companyId: 'linear', location: 'San Francisco, CA',
                    salary: '$200,000 – $260,000', workMode: 'Hybrid', type: 'full-time', experience: 'Manager',
                    posted: '3 days ago', skills: ['Engineering Leadership', 'People Management', 'Agile', 'React',
                        'TypeScript'],
                    description: 'Lead and grow a team of exceptional engineers building the future of project management. Balance technical excellence with people development in a high-autonomy environment.',
                    responsibilities: [
                        'Manage and mentor a team of 5-8 engineers',
                        'Drive technical strategy and architecture decisions',
                        'Conduct regular 1:1s and performance reviews',
                        'Collaborate with product and design on roadmap planning',
                        'Foster a culture of craftsmanship and continuous improvement'
                    ],
                    requirements: [
                        '7+ years of engineering experience with 2+ years in management',
                        'Strong technical background in web technologies',
                        'Proven track record of shipping high-quality products',
                        'Excellent people management and communication skills',
                        'Experience with developer tools or productivity software preferred'
                    ],
                    benefits: ['Top compensation', 'Significant equity', 'Health coverage', 'Executive coaching',
                        'Leadership development'
                    ] },
                { id: 24, title: 'Data Scientist', company: 'Render', companyId: 'render', location: 'San Francisco, CA',
                    salary: '$155,000 – $205,000', workMode: 'Hybrid', type: 'full-time', experience: 'Mid-Senior',
                    posted: '6 days ago', skills: ['Python', 'SQL', 'Machine Learning', 'Statistical Modeling',
                        'Data Visualization'],
                    description: 'Use data to improve how developers build and deploy on Render. Analyze usage patterns, build predictive models, and create dashboards that drive product decisions.',
                    responsibilities: [
                        'Analyze large datasets to identify usage patterns and trends',
                        'Build predictive models for capacity planning and optimization',
                        'Create dashboards and reports for product and leadership teams',
                        'Design and analyze A/B experiments',
                        'Collaborate with engineering on data infrastructure'
                    ],
                    requirements: [
                        '4+ years of data science experience',
                        'Strong programming skills in Python and SQL',
                        'Experience with statistical modeling and machine learning',
                        'Proficiency with data visualization tools',
                        'Ability to communicate findings to non-technical stakeholders'
                    ],
                    benefits: ['Competitive salary', 'Equity', 'Health benefits', 'Learning budget',
                        'Remote-friendly'
                    ] },
            ];

            // ── State ────────────────────────────
            let currentView = 'jobs';
            let currentJobDetailId = null;
            let currentCompanyDetailId = null;
            let currentCandidateTab = 'profile';
            let savedJobIds = new Set([1, 5, 10]);
            let applications = [
                { id: 101, jobId: 1, jobTitle: 'Senior Frontend Developer', company: 'Vercel', appliedDate: '2026-08-01',
                    status: 'interview' },
                { id: 102, jobId: 5, jobTitle: 'Full Stack Developer', company: 'Notion', appliedDate: '2026-07-28',
                    status: 'shortlisted' },
                { id: 103, jobId: 8, jobTitle: 'Security Engineer', company: 'Clerk', appliedDate: '2026-07-20',
                    status: 'pending' },
                { id: 104, jobId: 12, jobTitle: 'Product Manager', company: 'Linear', appliedDate: '2026-07-15',
                    status: 'rejected' },
                { id: 105, jobId: 3, jobTitle: 'Product Designer', company: 'Figma', appliedDate: '2026-06-10',
                    status: 'accepted' },
            ];
            let searchKeyword = '';
            let filterLocation = '';
            let filterType = '';
            let filterChip = 'all';
            let sortOrder = 'newest';
            let currentPage = 1;
            const pageSize = 8;
            let currentApplyJobId = null;

            // ── DOM References ────────────────────
            const $ = (sel) => document.querySelector(sel);
            const $$ = (sel) => document.querySelectorAll(sel);

            const appContainer = $('#appContainer');
            const viewJobs = $('#view-jobs');
            const viewJobDetail = $('#view-job-detail');
            const viewCompanies = $('#view-companies');
            const viewCompanyDetail = $('#view-company-detail');
            const viewSaved = $('#view-saved');
            const viewCandidate = $('#view-candidate');
            const jobList = $('#jobList');
            const savedJobList = $('#savedJobList');
            const savedEmpty = $('#savedEmpty');
            const resultCount = $('#resultCount');
            const pagination = $('#pagination');
            const companyGrid = $('#companyGrid');
            const candidateMain = $('#candidateMain');
            const searchKeywordInput = $('#searchKeyword');
            const filterLocationSelect = $('#filterLocation');
            const filterTypeSelect = $('#filterType');
            const filterChipsContainer = $('#filterChips');
            const applyModalOverlay = $('#applyModalOverlay');
            const toastContainer = $('#toastContainer');
            const filterDrawerOverlay = $('#filterDrawerOverlay');
            const filterDrawer = $('#filterDrawer');
            const navLinks = $('#navLinks');
            const mobileNavToggle = $('#mobileNavToggle');
            const btnMobileFilters = $('#btnMobileFilters');
            const drawerLocation = $('#drawerLocation');
            const drawerType = $('#drawerType');
            const drawerChips = $('#drawerChips');

            // ── Utility Functions ────────────────
            function showToast(message, type = '') {
                const toast = document.createElement('div');
                toast.className = 'toast ' + type;
                toast.textContent = message;
                toastContainer.appendChild(toast);
                setTimeout(() => {
                    toast.classList.add('fading');
                    setTimeout(() => toast.remove(), 300);
                }, 2200);
            }

            function getCompany(id) { return companies.find(c => c.id === id); }

            function getJob(id) { return jobs.find(j => j.id === id); }

            function formatSalary(s) { return s; }

            function getStatusClass(status) {
                const map = { applied: 'status-applied', pending: 'status-pending', shortlisted: 'status-shortlisted',
                    interview: 'status-interview', rejected: 'status-rejected', accepted: 'status-accepted' };
                return map[status] || 'status-applied';
            }

            function getStatusLabel(status) {
                return status.charAt(0).toUpperCase() + status.slice(1);
            }

            function getFilteredJobs() {
                let filtered = [...jobs];
                if (searchKeyword.trim()) {
                    const q = searchKeyword.toLowerCase().trim();
                    filtered = filtered.filter(j =>
                        j.title.toLowerCase().includes(q) ||
                        j.company.toLowerCase().includes(q) ||
                        j.skills.some(s => s.toLowerCase().includes(q)) ||
                        j.location.toLowerCase().includes(q)
                    );
                }
                if (filterLocation) {
                    if (filterLocation === 'remote') filtered = filtered.filter(j => j.workMode.toLowerCase() ===
                        'remote');
                    else filtered = filtered.filter(j => j.location.toLowerCase().includes(filterLocation.replace(
                        '-', ' ')));
                }
                if (filterType) {
                    filtered = filtered.filter(j => j.type === filterType);
                }
                if (filterChip !== 'all') {
                    const chipMap = {
                        remote: 'remote',
                        frontend: 'frontend',
                        backend: 'backend',
                        fullstack: 'full stack',
                        devops: 'devops',
                        data: 'data',
                        design: 'design'
                    };
                    const keyword = chipMap[filterChip] || filterChip;
                    filtered = filtered.filter(j =>
                        j.title.toLowerCase().includes(keyword) ||
                        j.skills.some(s => s.toLowerCase().includes(keyword))
                    );
                }
                if (sortOrder === 'newest') filtered.sort((a, b) => a.id - b.id);
                else if (sortOrder === 'oldest') filtered.sort((a, b) => b.id - a.id);
                else if (sortOrder === 'salary-high') filtered.sort((a, b) => {
                    const getMax = (s) => { const m = s.match(/[\d,]+/g); return m ? parseInt(m[m.length - 1]
                        .replace(/,/g, '')) : 0; };
                    return getMax(b.salary) - getMax(a.salary);
                });
                return filtered;
            }

            function getPageData(filtered) {
                const total = filtered.length;
                const totalPages = Math.ceil(total / pageSize);
                const start = (currentPage - 1) * pageSize;
                const pageJobs = filtered.slice(start, start + pageSize);
                return { pageJobs, total, totalPages, start };
            }

            // ── Render Functions ──────────────────
            function renderJobCard(job, showSave = true) {
                const isSaved = savedJobIds.has(job.id);
                const companyData = getCompany(job.companyId);
                const logoLetter = companyData ? companyData.logo : job.company.charAt(0);
                return `
                <div class="job-card" data-job-id="${job.id}" role="listitem">
                    <div class="job-card-avatar">${logoLetter}</div>
                    <div class="job-card-body">
                        <div class="job-card-title">${job.title}</div>
                        <div class="job-card-company">${job.company}</div>
                        <div class="job-card-meta">
                            <span>📍 ${job.location}</span>
                            <span>💰 ${job.salary}</span>
                            <span>🏢 ${job.workMode}</span>
                            <span>⏱ ${job.posted}</span>
                        </div>
                        <div class="job-card-tags">
                            ${job.skills.slice(0, 4).map(s => `<span class="tag">${s}</span>`).join('')}
                            ${job.skills.length > 4 ? `<span class="tag">+${job.skills.length - 4}</span>` : ''}
                        </div>
                    </div>
                    ${showSave ? `<button class="job-card-save ${isSaved ? 'saved' : ''}" data-save-job="${job.id}" aria-label="${isSaved ? 'Unsave' : 'Save'} job">
                        ${isSaved ? '★' : '☆'}
                    </button>` : ''}
                </div>`;
            }

            function renderJobList(targetEl, filtered, showSave = true) {
                const { pageJobs, total, totalPages, start } = getPageData(filtered);
                if (pageJobs.length === 0) {
                    targetEl.innerHTML =
                        `<div class="empty-state"><svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg><h3>No jobs found</h3><p>Try adjusting your search or filters.</p></div>`;
                } else {
                    targetEl.innerHTML = pageJobs.map(j => renderJobCard(j, showSave)).join('');
                }
                return { total, totalPages, pageJobs };
            }

            function renderPagination(totalPages) {
                if (totalPages <= 1) { pagination.innerHTML = ''; return; }
                let html = '';
                html +=
                    `<button ${currentPage === 1 ? 'disabled' : ''} data-page="${currentPage - 1}" aria-label="Previous page">← Prev</button>`;
                for (let i = 1; i <= totalPages; i++) {
                    html +=
                        `<button class="${i === currentPage ? 'active' : ''}" data-page="${i}" aria-label="Page ${i}">${i}</button>`;
                }
                html +=
                    `<button ${currentPage === totalPages ? 'disabled' : ''} data-page="${currentPage + 1}" aria-label="Next page">Next →</button>`;
                pagination.innerHTML = html;
            }

            function refreshJobListView() {
                const filtered = getFilteredJobs();
                const { total, totalPages } = renderJobList(jobList, filtered, true);
                resultCount.textContent = `Showing ${filtered.length} job${filtered.length !== 1 ? 's' : ''}`;
                renderPagination(totalPages);
            }

            function refreshSavedView() {
                const savedJobs = jobs.filter(j => savedJobIds.has(j.id));
                if (savedJobs.length === 0) {
                    savedJobList.innerHTML = '';
                    savedEmpty.classList.remove('hidden');
                    savedJobList.style.display = 'none';
                } else {
                    savedEmpty.classList.add('hidden');
                    savedJobList.style.display = '';
                    renderJobList(savedJobList, savedJobs, true);
                }
            }

            function renderJobDetail(jobId) {
                const job = getJob(jobId);
                if (!job) return;
                const companyData = getCompany(job.companyId);
                const isSaved = savedJobIds.has(job.id);
                currentJobDetailId = jobId;
                viewJobDetail.innerHTML = `
                <div class="breadcrumbs">
                    <a href="#" data-view="jobs">Jobs</a> <span class="sep">›</span>
                    <a href="#" data-view="companies" data-company="${job.companyId}">${job.company}</a> <span class="sep">›</span>
                    <span>${job.title}</span>
                </div>
                <div class="job-detail-layout">
                    <div class="job-detail-main">
                        <h2>${job.title}</h2>
                        <div class="job-detail-company-row">
                            <div class="job-card-avatar">${companyData ? companyData.logo : job.company.charAt(0)}</div>
                            <span>${job.company}</span>
                        </div>
                        <div class="job-detail-meta-row">
                            <span>📍 ${job.location}</span>
                            <span>💰 ${job.salary}</span>
                            <span>🏢 ${job.workMode}</span>
                            <span>📋 ${job.type.replace('-', ' ')}</span>
                            <span>🎯 ${job.experience}</span>
                            <span>⏱ Posted ${job.posted}</span>
                        </div>
                        <div class="job-detail-section">
                            <h3>Description</h3>
                            <p>${job.description}</p>
                        </div>
                        <div class="job-detail-section">
                            <h3>Responsibilities</h3>
                            <ul>${job.responsibilities.map(r => `<li>${r}</li>`).join('')}</ul>
                        </div>
                        <div class="job-detail-section">
                            <h3>Requirements</h3>
                            <ul>${job.requirements.map(r => `<li>${r}</li>`).join('')}</ul>
                        </div>
                        <div class="job-detail-section">
                            <h3>Skills</h3>
                            <div class="skills-grid">${job.skills.map(s => `<span class="tag">${s}</span>`).join('')}</div>
                        </div>
                        <div class="job-detail-section">
                            <h3>Benefits</h3>
                            <ul>${job.benefits.map(b => `<li>${b}</li>`).join('')}</ul>
                        </div>
                    </div>
                    <aside class="job-detail-sidebar">
                        <div class="sidebar-card">
                            <h4>${job.company}</h4>
                            ${companyData ? `
                            <div class="sidebar-info-row"><span class="label">Website</span><span>${companyData.website}</span></div>
                            <div class="sidebar-info-row"><span class="label">Location</span><span>${companyData.location}</span></div>
                            <div class="sidebar-info-row"><span class="label">Size</span><span>${companyData.size}</span></div>
                            <div class="sidebar-info-row"><span class="label">Industry</span><span>${companyData.industry}</span></div>
                            ` : ''}
                            <div class="sidebar-actions">
                                <button class="btn btn-primary btn-full" data-apply="${job.id}">Apply Now</button>
                                <button class="btn btn-outline btn-full" data-save-job="${job.id}">${isSaved ? '★ Saved' : '☆ Save Job'}</button>
                            </div>
                        </div>
                        <div class="sidebar-card">
                            <h4>Job Details</h4>
                            <div class="sidebar-info-row"><span class="label">Type</span><span>${job.type.replace('-', ' ')}</span></div>
                            <div class="sidebar-info-row"><span class="label">Experience</span><span>${job.experience}</span></div>
                            <div class="sidebar-info-row"><span class="label">Work Mode</span><span>${job.workMode}</span></div>
                            <div class="sidebar-info-row"><span class="label">Posted</span><span>${job.posted}</span></div>
                        </div>
                    </aside>
                </div>`;
                switchView('job-detail');
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }

            function renderCompanyDirectory() {
                companyGrid.innerHTML = companies.map(c => `
                <a href="#" class="company-card" data-company="${c.id}">
                    <div class="company-card-header">
                        <div class="company-card-logo">${c.logo}</div>
                        <div class="company-card-name">${c.name}</div>
                    </div>
                    <div class="company-card-desc">${c.desc}</div>
                    <div class="company-card-meta">
                        <span>📍 ${c.location}</span>
                        <span>👥 ${c.size}</span>
                        <span>📋 ${c.openPositions} open positions</span>
                    </div>
                </a>`).join('');
            }

            function renderCompanyDetail(companyId) {
                const company = getCompany(companyId);
                if (!company) return;
                currentCompanyDetailId = companyId;
                const companyJobs = jobs.filter(j => j.companyId === companyId);
                viewCompanyDetail.innerHTML = `
                <div class="breadcrumbs">
                    <a href="#" data-view="companies">Companies</a> <span class="sep">›</span>
                    <span>${company.name}</span>
                </div>
                <div class="job-detail-layout">
                    <div class="job-detail-main">
                        <div style="display:flex;align-items:center;gap:14px;margin-bottom:16px;">
                            <div class="company-card-logo" style="width:56px;height:56px;font-size:1.3rem;">${company.logo}</div>
                            <div>
                                <h2 style="margin-bottom:2px;">${company.name}</h2>
                                <a href="https://${company.website}" target="_blank" rel="noopener" style="font-size:0.85rem;">${company.website} ↗</a>
                            </div>
                        </div>
                        <div class="job-detail-meta-row">
                            <span>📍 ${company.location}</span>
                            <span>👥 ${company.size} employees</span>
                            <span>🏭 ${company.industry}</span>
                            <span>📋 ${company.openPositions} open positions</span>
                        </div>
                        <div class="job-detail-section">
                            <h3>About</h3>
                            <p>${company.overview}</p>
                        </div>
                        <div class="job-detail-section">
                            <h3>Open Positions (${companyJobs.length})</h3>
                            <div class="job-list" style="border-radius:var(--radius-md);">${companyJobs.map(j => renderJobCard(j, true)).join('')}</div>
                        </div>
                    </div>
                    <aside class="job-detail-sidebar">
                        <div class="sidebar-card">
                            <h4>Company Info</h4>
                            <div class="sidebar-info-row"><span class="label">Website</span><span>${company.website}</span></div>
                            <div class="sidebar-info-row"><span class="label">Location</span><span>${company.location}</span></div>
                            <div class="sidebar-info-row"><span class="label">Size</span><span>${company.size}</span></div>
                            <div class="sidebar-info-row"><span class="label">Industry</span><span>${company.industry}</span></div>
                            <div class="sidebar-info-row"><span class="label">Open Positions</span><span>${company.openPositions}</span></div>
                        </div>
                    </aside>
                </div>`;
                switchView('company-detail');
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }

            function renderCandidateTab(tab) {
                currentCandidateTab = tab;
                let html = '';
                if (tab === 'profile') {
                    html = `
                    <h3 style="margin-bottom:16px;">Profile</h3>
                    <div style="display:grid;gap:12px;">
                        <div><strong>Name:</strong> Alex Kim</div>
                        <div><strong>Email:</strong> alex.kim@example.com</div>
                        <div><strong>Location:</strong> San Francisco, CA</div>
                        <div><strong>Title:</strong> Full Stack Developer</div>
                        <div><strong>Experience:</strong> 6 years</div>
                        <div><strong>Skills:</strong> React, TypeScript, Node.js, PostgreSQL, GraphQL, AWS</div>
                        <div><strong>Resume:</strong> <a href="#">resume-alex-kim.pdf</a></div>
                        <div style="margin-top:8px;"><strong>Profile Completion:</strong> 85%</div>
                        <div style="background:var(--color-border-light);border-radius:20px;height:8px;overflow:hidden;max-width:300px;">
                            <div style="width:85%;height:100%;background:var(--color-success);border-radius:20px;"></div>
                        </div>
                    </div>`;
                } else if (tab === 'applications') {
                    html = `
                    <h3 style="margin-bottom:14px;">Applications (${applications.length})</h3>
                    <div style="overflow-x:auto;">
                    <table class="app-table">
                        <thead><tr><th>Job</th><th>Company</th><th>Applied</th><th>Status</th></tr></thead>
                        <tbody>${applications.map(a => `
                            <tr>
                                <td><a href="#" data-view-job="${a.jobId}">${a.jobTitle}</a></td>
                                <td>${a.company}</td>
                                <td>${a.appliedDate}</td>
                                <td><span class="status-badge ${getStatusClass(a.status)}">${getStatusLabel(a.status)}</span></td>
                            </tr>`).join('')}</tbody>
                    </table></div>`;
                } else if (tab === 'saved-candidate') {
                    const saved = jobs.filter(j => savedJobIds.has(j.id));
                    if (saved.length === 0) {
                        html =
                            `<div class="empty-state"><svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2z"/></svg><h3>No saved jobs</h3><p>Save jobs to view them here.</p></div>`;
                    } else {
                        html =
                            `<h3 style="margin-bottom:14px;">Saved Jobs (${saved.length})</h3><div class="job-list" style="border-radius:var(--radius-md);">${saved.map(j => renderJobCard(j, true)).join('')}</div>`;
                    }
                }
                candidateMain.innerHTML = html;
            }

            function switchView(viewName) {
                currentView = viewName;
                [viewJobs, viewJobDetail, viewCompanies, viewCompanyDetail, viewSaved, viewCandidate].forEach(v => v
                    .classList.remove('active'));
                if (viewName === 'jobs') viewJobs.classList.add('active');
                else if (viewName === 'job-detail') viewJobDetail.classList.add('active');
                else if (viewName === 'companies') viewCompanies.classList.add('active');
                else if (viewName === 'company-detail') viewCompanyDetail.classList.add('active');
                else if (viewName === 'saved') viewSaved.classList.add('active');
                else if (viewName === 'candidate') viewCandidate.classList.add('active');

                $$('.nav-link').forEach(l => l.classList.remove('active'));
                const navMap = { jobs: 'Jobs', 'job-detail': 'Jobs', companies: 'Companies', 'company-detail': 'Companies',
                    saved: 'Saved Jobs', candidate: 'Candidate' };
                const targetLabel = navMap[viewName] || 'Jobs';
                $$('.nav-link').forEach(l => { if (l.textContent.trim() === targetLabel) l.classList.add('active'); });

                if (viewName === 'jobs') refreshJobListView();
                if (viewName === 'saved') refreshSavedView();
                if (viewName === 'candidate') renderCandidateTab(currentCandidateTab);
                if (viewName === 'companies') renderCompanyDirectory();
                appContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }

            // ── Event Handlers ────────────────────
            function handleViewSwitch(e) {
                const target = e.target.closest('[data-view]');
                if (!target) return;
                e.preventDefault();
                const view = target.dataset.view;
                const companyId = target.dataset.company;
                const jobId = target.dataset.viewJob;
                if (jobId) { renderJobDetail(parseInt(jobId));
                    return; }
                if (companyId) { renderCompanyDetail(companyId);
                    return; }
                if (view === 'job-detail' && currentJobDetailId) { renderJobDetail(currentJobDetailId); return; }
                switchView(view);
                navLinks.classList.remove('open');
                mobileNavToggle.setAttribute('aria-expanded', 'false');
            }

            function handleJobCardClick(e) {
                const card = e.target.closest('.job-card');
                if (!card) return;
                if (e.target.closest('[data-save-job]')) return;
                const jobId = parseInt(card.dataset.jobId);
                if (jobId) renderJobDetail(jobId);
            }

            function handleSaveJob(e) {
                const btn = e.target.closest('[data-save-job]');
                if (!btn) return;
                e.preventDefault();
                e.stopPropagation();
                const jobId = parseInt(btn.dataset.saveJob);
                if (savedJobIds.has(jobId)) {
                    savedJobIds.delete(jobId);
                    btn.classList.remove('saved');
                    btn.innerHTML = '☆';
                    showToast('Job removed from saved', '');
                } else {
                    savedJobIds.add(jobId);
                    btn.classList.add('saved');
                    btn.innerHTML = '★';
                    showToast('Job saved!', 'success');
                }
                if (currentView === 'saved') refreshSavedView();
                if (currentView === 'job-detail' && currentJobDetailId === jobId) renderJobDetail(jobId);
                if (currentView === 'candidate' && currentCandidateTab === 'saved-candidate') renderCandidateTab(
                    'saved-candidate');
                refreshJobListView();
            }

            function handleApply(e) {
                const btn = e.target.closest('[data-apply]');
                if (!btn) return;
                e.preventDefault();
                currentApplyJobId = parseInt(btn.dataset.apply);
                const job = getJob(currentApplyJobId);
                if (job) {
                    $('#applyModalTitle').textContent = `Apply for ${job.title} at ${job.company}`;
                }
                applyModalOverlay.classList.remove('hidden');
                document.body.style.overflow = 'hidden';
            }

            function closeApplyModal() {
                applyModalOverlay.classList.add('hidden');
                document.body.style.overflow = '';
                currentApplyJobId = null;
            }

            function submitApplication() {
                if (currentApplyJobId) {
                    const job = getJob(currentApplyJobId);
                    const newApp = {
                        id: Date.now(),
                        jobId: currentApplyJobId,
                        jobTitle: job ? job.title : 'Unknown Position',
                        company: job ? job.company : 'Unknown Company',
                        appliedDate: new Date().toISOString().split('T')[0],
                        status: 'applied'
                    };
                    applications.unshift(newApp);
                    showToast('Application submitted successfully!', 'success');
                }
                closeApplyModal();
                if (currentView === 'candidate') renderCandidateTab(currentCandidateTab);
            }

            function handleSearch() {
                searchKeyword = searchKeywordInput.value;
                currentPage = 1;
                refreshJobListView();
            }

            function handleFilterChange() {
                filterLocation = filterLocationSelect.value;
                filterType = filterTypeSelect.value;
                currentPage = 1;
                refreshJobListView();
            }

            function handleChipClick(e) {
                const chip = e.target.closest('.chip');
                if (!chip) return;
                filterChip = chip.dataset.chip;
                currentPage = 1;
                $$('.chip').forEach(c => c.classList.remove('active'));
                chip.classList.add('active');
                refreshJobListView();
            }

            function handlePaginationClick(e) {
                const btn = e.target.closest('button');
                if (!btn || !btn.dataset.page) return;
                currentPage = parseInt(btn.dataset.page);
                refreshJobListView();
                jobList.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }

            function handleCandidateNav(e) {
                const link = e.target.closest('[data-candidate-tab]');
                if (!link) return;
                e.preventDefault();
                const tab = link.dataset.candidateTab;
                $$('#candidateNav a').forEach(a => a.classList.remove('active'));
                link.classList.add('active');
                renderCandidateTab(tab);
            }

            function handleMobileNavToggle() {
                const isOpen = navLinks.classList.toggle('open');
                mobileNavToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
            }

            function handleMobileFilters() {
                drawerLocation.value = filterLocation;
                drawerType.value = filterType;
                drawerChips.innerHTML = ['all', 'remote', 'frontend', 'backend', 'fullstack', 'devops', 'data',
                    'design'
                ].map(chip =>
                    `<button class="chip ${filterChip === chip ? 'active' : ''}" data-drawer-chip="${chip}">${chip.charAt(0).toUpperCase() + chip.slice(1)}</button>`
                ).join('');
                filterDrawerOverlay.classList.add('open');
                filterDrawer.classList.add('open');
                document.body.style.overflow = 'hidden';
            }

            function closeDrawer() {
                filterDrawerOverlay.classList.remove('open');
                filterDrawer.classList.remove('open');
                document.body.style.overflow = '';
            }

            function applyDrawerFilters() {
                filterLocation = drawerLocation.value;
                filterType = drawerType.value;
                const activeChip = drawerChips.querySelector('.chip.active');
                if (activeChip) filterChip = activeChip.dataset.drawerChip;
                filterLocationSelect.value = filterLocation;
                filterTypeSelect.value = filterType;
                $$('#filterChips .chip').forEach(c => c.classList.remove('active'));
                const mainChip = document.querySelector(`#filterChips .chip[data-chip="${filterChip}"]`);
                if (mainChip) mainChip.classList.add('active');
                currentPage = 1;
                refreshJobListView();
                closeDrawer();
            }

            function handleDrawerChipClick(e) {
                const chip = e.target.closest('.chip');
                if (!chip || !chip.dataset.drawerChip) return;
                $$('#drawerChips .chip').forEach(c => c.classList.remove('active'));
                chip.classList.add('active');
                filterChip = chip.dataset.drawerChip;
            }

            function handleNotificationsClick() {
                showToast('You have 3 new job alerts', '');
            }

            function handleClickOutsideModal(e) {
                if (e.target === applyModalOverlay) closeApplyModal();
                if (e.target === filterDrawerOverlay) closeDrawer();
            }

            function handleKeydown(e) {
                if (e.key === 'Escape') {
                    if (!applyModalOverlay.classList.contains('hidden')) closeApplyModal();
                    if (filterDrawerOverlay.classList.contains('open')) closeDrawer();
                }
            }

            // ── Initialize ────────────────────────
            function init() {
                // Set initial filter values
                filterLocationSelect.value = '';
                filterTypeSelect.value = '';
                searchKeywordInput.value = '';

                // Render initial views
                refreshJobListView();
                renderCompanyDirectory();
                refreshSavedView();
                renderCandidateTab('profile');

                // Event listeners
                document.addEventListener('click', function(e) {
                    handleViewSwitch(e);
                    handleJobCardClick(e);
                    handleSaveJob(e);
                    handleApply(e);
                    handleChipClick(e);
                    handlePaginationClick(e);
                    handleCandidateNav(e);
                    handleClickOutsideModal(e);
                    handleDrawerChipClick(e);
                });

                searchKeywordInput.addEventListener('input', debounce(handleSearch, 250));
                filterLocationSelect.addEventListener('change', handleFilterChange);
                filterTypeSelect.addEventListener('change', handleFilterChange);
                mobileNavToggle.addEventListener('click', handleMobileNavToggle);
                btnMobileFilters.addEventListener('click', handleMobileFilters);
                $('#btnCloseDrawer').addEventListener('click', closeDrawer);
                $('#btnApplyDrawerFilters').addEventListener('click', applyDrawerFilters);
                $('#btnCancelApply').addEventListener('click', closeApplyModal);
                $('#btnSubmitApply').addEventListener('click', submitApplication);
                $('#btnNotifications').addEventListener('click', handleNotificationsClick);
                document.addEventListener('keydown', handleKeydown);

                // Responsive: show mobile filter button
                function updateMobileFilterBtn() {
                    if (window.innerWidth <= 768) {
                        btnMobileFilters.style.display = 'inline-flex';
                    } else {
                        btnMobileFilters.style.display = 'none';
                    }
                }
                updateMobileFilterBtn();
                window.addEventListener('resize', debounce(updateMobileFilterBtn, 150));

                // Initial saved jobs view check
                refreshSavedView();
            }

            function debounce(fn, delay) {
                let timer;
                return function(...args) {
                    clearTimeout(timer);
                    timer = setTimeout(() => fn.apply(this, args), delay);
                };
            }

            // Start the app
            init();
            console.log('DevSnips Job Board — Ready');
        })();
