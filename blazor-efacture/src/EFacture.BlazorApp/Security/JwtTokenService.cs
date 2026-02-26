using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;

namespace EFacture.BlazorApp.Security;

public class JwtTokenService(IConfiguration configuration)
{
    public string Generate(string username, string role)
    {
        var key = configuration["Jwt:Key"] ?? "dev-ultra-secret-key-change-me";
        var credentials = new SigningCredentials(new SymmetricSecurityKey(Encoding.UTF8.GetBytes(key)), SecurityAlgorithms.HmacSha256);

        var token = new JwtSecurityToken(
            claims:
            [
                new Claim(ClaimTypes.Name, username),
                new Claim(ClaimTypes.Role, role)
            ],
            expires: DateTime.UtcNow.AddMinutes(30),
            signingCredentials: credentials
        );

        return new JwtSecurityTokenHandler().WriteToken(token);
    }
}
