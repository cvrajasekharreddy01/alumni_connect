from profiles.models import StudentProfile, AlumniProfile

class MatchingService:
    @staticmethod
    def calculate_match_score(student, alumni):
        """
        Scoring logic:
        Final Score = 0.5 * skill_match + 0.3 * career_match + 0.2 * department_match
        """
        try:
            s_profile = student.student_profile
        except (AttributeError, StudentProfile.DoesNotExist):
            return 0, []
            
        try:
            a_profile = alumni.alumni_profile
        except (AttributeError, AlumniProfile.DoesNotExist):
            return 0, []

        # Skill matching (Jaccard similarity approximation)
        s_skills = set(s_profile.skills) if s_profile.skills else set()
        a_skills = set(a_profile.skills) if a_profile.skills else set()
        
        if not s_skills:
            skill_score = 0
        else:
            intersection = s_skills.intersection(a_skills)
            skill_score = len(intersection) / len(s_skills)

        # Career match
        s_interest = (s_profile.career_interest or "").lower()
        a_industry = (a_profile.industry or "").lower()
        a_role = (a_profile.job_role or "").lower()
        
        career_score = 1.0 if s_interest and (s_interest in a_industry or s_interest in a_role) else 0.0

        # Department match
        s_dept = (s_profile.department or "").lower()
        a_dept = (getattr(a_profile, 'department', None) or "").lower()
        
        if s_dept and a_dept:
            dept_score = 1.0 if s_dept == a_dept else 0.0
        else:
            dept_score = 0.0

        final_score = (0.5 * skill_score) + (0.3 * career_score) + (0.2 * dept_score)
        
        reasons = []
        if skill_score > 0.5: reasons.append("Strong skill overlap")
        if career_score > 0: reasons.append(f"Alumni works in {a_profile.industry or 'relevant industry'}")
        if dept_score > 0: reasons.append("Same department")

        return round(final_score, 2), reasons

    @staticmethod
    def get_recommendations(student, limit=5):
        alumni_list = AlumniProfile.objects.exclude(user=student)
        recommendations = []
        for a_profile in alumni_list:
            score, reasons = MatchingService.calculate_match_score(student, a_profile.user)
            if score > 0:
                recommendations.append({
                    'alumni': a_profile.user,
                    'score': score,
                    'reasons': ", ".join(reasons)
                })
        
        return sorted(recommendations, key=lambda x: x['score'], reverse=True)[:limit]
