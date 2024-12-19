import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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



def create_comparative_charts(df, group_by_columns=['experience', 'job_location'], max_skills=20):
    """
    Creates a set of grouped charts for salary, experience, and skills.

    Args:
    df (DataFrame): The job data.
    group_by_columns (list): List of columns to group by for comparison.
    max_skills (int): Number of top skills to display.

    Returns:
    None
    """
    # Initialize subplots layout
    n_cols = len(group_by_columns)
    fig = make_subplots(
        rows=4, cols=n_cols, 
        subplot_titles=[
            f"{chart} grouped by {group}" 
            for chart in ["Job Count", "Salary Distribution", "Experience Distribution", "Skill Distribution"]
            for group in group_by_columns
        ],
        horizontal_spacing=0.1,
        vertical_spacing=0.15,
    )

    # Iterate over group_by_columns
    for idx, group_by in enumerate(group_by_columns):
        col_idx = idx + 1

        # Job count by group
        job_counts = df[group_by].value_counts().reset_index()
        job_counts.columns = [group_by, 'count']
        fig_job_counts = px.bar(job_counts, x=group_by, y='count', 
                                color=group_by, 
                                labels={group_by: group_by.title(), 'count': 'Job Count'})
        for trace in fig_job_counts.data:
            fig.add_trace(trace, row=1, col=col_idx)

        # Salary distribution
        fig_salary = px.box(df, x=group_by, y='standardize_salary_VND', 
                            color=group_by, 
                            labels={group_by: group_by.title(), 'standardize_salary_VND': 'Salary in VND'})
        for trace in fig_salary.data:
            fig.add_trace(trace, row=2, col=col_idx)

        # Experience distribution
        experience_counts = df['experience'].value_counts().reset_index()
        experience_counts.columns = ['experience', 'count']
        fig_experience = px.pie(experience_counts, values='count', names='experience', 
                                hole=0.3)
        for trace in fig_experience.data:
            fig.add_trace(trace, row=3, col=col_idx)

        # Skill distribution
        skills = df['requirement'].dropna().str.split(',').explode().str.strip()
        skill_counts = skills.value_counts().head(max_skills).reset_index()
        skill_counts.columns = ['skill', 'count']
        fig_skills = px.bar(skill_counts, x='skill', y='count', 
                            color='skill', 
                            labels={'skill': 'Skill', 'count': 'Count'})
        for trace in fig_skills.data:
            fig.add_trace(trace, row=4, col=col_idx)

    # Update layout
    fig.update_layout(
        height=1200, width=300 * n_cols,
        title_text="Job Analysis by Various Groups",
        showlegend=False,
    )

    fig.show()
