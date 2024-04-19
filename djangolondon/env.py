from dataclasses import dataclass, fields


from dotenv import dotenv_values


@dataclass
class Env:
    MEETUP_COM_KEY: str
    MEETUP_COM_SECRET: str
    MEETUP_COM_REDIRECT_URI: str
    OPENAI_API_KEY: str

    def __repr__(self):
        sensitive_keywords = ["KEY", "PASSWORD", "SECRET", "TOKEN"]
        return (
            type(self).__name__
            + "("
            + ", ".join(
                (
                    f"{field.name}='****'"
                    if any(kw in field.name for kw in sensitive_keywords)
                    else f"{field.name}='{getattr(self, field.name)}'"
                )
                for field in fields(self)
            )
            + ")"
        )

    @classmethod
    def get_env(cls):
        return cls(**dotenv_values(".env"))
