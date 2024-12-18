import plotly.express as px
import plotly.graph_objects as go

def create_charts(df):
    job_counts = df['category'].value_counts().reset_index()
    job_counts.columns = ['category', 'count']

    fig_job_counts = px.bar(job_counts, x='category', y='count', 
                            title='Job count by position',
                            labels={'category': 'Category of job position', 'count': 'Number of job post'},
                            color='category')
    fig_job_counts.update_layout(xaxis_tickangle=-45)

    # Salary distribution by category
    fig_salary_distribution = px.box(df, x='category', y='standardize_salary_VND', 
                                    title='Salary distribution by category',
                                    labels={'category': 'Category of job position', 'standardize_salary_VND': 'Salary in VND'},
                                    color='category')

    # Experience requirement
    experience_counts = df['experience'].value_counts().reset_index()
    experience_counts.columns = ['experience', 'count']
    fig_experience_counts = px.pie(experience_counts, values='count', names='experience', 
                                title='Experience Requirement',
                                hole=0.3)

    # Location distribution
    location_counts = df['job_location'].value_counts().reset_index()
    location_counts.columns = ['location', 'count']
    fig_location_counts = px.bar(location_counts, x='location', y='count', 
                                title='Job distribution by location',
                                labels={'location': 'Location', 'count': 'Number of job post'},
                                color='location')
    fig_location_counts.update_layout(xaxis_tickangle=-45)

    # Required skills
    skills = df['requirement'].dropna().str.split(',').explode().str.strip()
    skill_counts = skills.value_counts().reset_index()
    skill_counts.columns = ['skill', 'count']
    fig_skill_counts = px.bar(skill_counts.head(20), x='skill', y='count', 
                            title='Top 20 most required skills',
                            labels={'skill': 'Skill', 'count': 'Count'},
                            color='skill')
    fig_skill_counts.update_layout(xaxis_tickangle=-45)

    # Show all charts
    fig_job_counts.show()
    fig_salary_distribution.show()
    fig_experience_counts.show()
    fig_location_counts.show()
    fig_skill_counts.show()

    return None
